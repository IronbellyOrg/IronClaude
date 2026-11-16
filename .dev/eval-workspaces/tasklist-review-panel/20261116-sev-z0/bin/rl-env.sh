#!/usr/bin/env bash
# Sourced by every RL script before bin/common.sh (DESIGN 1.2 K9, TESTING 1.3).
# Own sandbox root: the sibling's root is refused with exit 4. Test hook: RL_FORCE_EXC.
SW_SB_ROOT=${SW_SB_ROOT:-/tmp/evalsb-recipe}
export SW_SB_ROOT

_rl_root=$(realpath -m -- "$SW_SB_ROOT")
case "$_rl_root/" in
  /tmp/evalsb-sweep/*)
    echo "E_SIBLING_ROOT: SW_SB_ROOT=$SW_SB_ROOT is the Sweep Sheet sandbox root" >&2
    exit 4
    ;;
esac
unset _rl_root

# The one test hook: raise in one component. Anything else is refused.
case "${RL_FORCE_EXC:-}" in
  "" | lens | check | reask) ;;
  *)
    echo "E_HOOK: RL_FORCE_EXC=${RL_FORCE_EXC} is not one of lens, check, reask" >&2
    exit 2
    ;;
esac
