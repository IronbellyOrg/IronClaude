#!/usr/bin/env bash
# Sourced by every shell file of the Sweep Sheet harness (DESIGN 1.2 K1, K2; 2.3).
# SW is the folder of this build; REPO is four levels above it.
SW=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)
REPO=$(cd "$SW/../../../.." && pwd -P)
EVAL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
SB=${SW_SB_ROOT:-/tmp/evalsb-sweep}
SRC_REPO=${SW_SRC_REPO:-$REPO}
export PYTHONDONTWRITEBYTECODE=1
export SUPERCLAUDE_CODEGRAPH_AUTOINIT=0
# The four reviewer models (K2). The judge model is named only in bin/judge-one.sh.
ALLOWED_MODELS="muse-ember-1.0 gpt-6-luna claude-haiku-5-5 claude-sonnet-5-5 gpt-6.1-sol muse-wonder-1.0"

sw_now() { date +%s.%3N; }

# Refuse any output path outside SW, SB or /tmp (K1). Resolves symlinks and "..".
sw_assert_writable() {
  local p rp root
  p=$1
  rp=$(realpath -m -- "$p") || return 1
  for root in "$(realpath -m -- "$SW")" "$(realpath -m -- "$SB")"; do
    case "$rp/" in "$root"/*) return 0 ;; esac
  done
  case "$rp/" in /tmp/?*) return 0 ;; esac
  echo "E_NOT_WRITABLE: $p (resolves to $rp)" >&2
  return 1
}

# sw_assert_override NAME [VALUE]: VALUE defaults to the environment value of NAME.
# Each override is judged by its kind. Unknown names are refused.
sw_assert_override() {
  local name=$1 val rp
  if [ $# -ge 2 ]; then val=$2; else val=${!name:-}; fi
  case "$name" in
    SW_SB_ROOT | SW_SRC_REPO)
      rp=$(realpath -m -- "$val") || return 1
      case "$rp/" in
        /tmp/?*) return 0 ;;
      esac
      echo "E_OVERRIDE: $name=$val is outside /tmp/" >&2
      return 1
      ;;
    SW_KILL_S)
      if [[ $val =~ ^[0-9]+(\.[0-9]+)?$ ]] && awk -v v="$val" 'BEGIN{exit !(v >= 0.1 && v <= 15)}'; then
        return 0
      fi
      echo "E_OVERRIDE: $name=$val is not a number from 0.1 to 15" >&2
      return 1
      ;;
    SW_PREPASS_CMD)
      # Stubs of the kill test only: "sleep <n>" or "false", plain words, no shell syntax.
      if [[ $val =~ ^(sleep|false)([[:space:]]+[A-Za-z0-9._-]+)*$ ]]; then
        return 0
      fi
      echo "E_OVERRIDE: $name=$val is not a sleep or false stub" >&2
      return 1
      ;;
    SW_RENDER_CMD)
      # Stub of the render-failure test only (Task 27): the SS brief render of bin/run-panel.sh becomes `false`.
      if [[ $val == false ]]; then
        return 0
      fi
      echo "E_OVERRIDE: $name=$val is not the false stub" >&2
      return 1
      ;;
    SW_PANELS)
      # The panel file of one schedule run (Task 32): bin/run-schedule.sh writes the spike fallback caps into a copy of
      # config/panels.json under SW/runs/ and points the runs at it; tests keep theirs under /tmp/.
      rp=$(realpath -m -- "$val") || return 1
      case "$rp/" in
        /tmp/?* | "$SW"/runs/?*) return 0 ;;
      esac
      echo "E_OVERRIDE: $name=$val is outside /tmp/ and $SW/runs/" >&2
      return 1
      ;;
  esac
  echo "E_OVERRIDE: $name is not a known override" >&2
  return 1
}

# Check every override that is set in the environment.
sw_assert_overrides() {
  local v rc=0
  for v in SW_SB_ROOT SW_SRC_REPO SW_KILL_S SW_PREPASS_CMD SW_RENDER_CMD SW_PANELS; do
    [ -n "${!v:-}" ] || continue
    sw_assert_override "$v" || rc=1
  done
  return $rc
}

# Reviewer model allowlist: exact match, nothing else (K2).
sw_assert_model() {
  local m=${1:-} a
  [ -n "$m" ] || { echo "E_MODEL: empty model id" >&2; return 1; }
  for a in $ALLOWED_MODELS; do
    [ "$m" = "$a" ] && return 0
  done
  echo "E_MODEL: $m is not an allowed reviewer model" >&2
  return 1
}

# Counted runs use one attempt (DD-8).
sw_assert_nofallback() {
  [ "${NOFALLBACK:-}" = "1" ] || { echo "E_NOFALLBACK: NOFALLBACK=1 is required" >&2; return 1; }
}

sw_py() { uv run --frozen --project "$REPO" python "$@"; }

# A bad override stops the sourcing shell: nothing runs on an unchecked override.
sw_assert_overrides || exit 1
