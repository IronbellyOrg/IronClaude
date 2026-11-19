7e6f69c5c2938b68f592a8ec66bccfcb44b71815

# Family probe probe-1-1.md (failing review r1-1)

## family: gh-refuse-case
defect form: a case-sensitive glob asked to implement a case-insensitive refusal.
search command: grep -n -i -e 'superclaude' .dev/issues/442/scripts/lib.sh
before-output (touched files):
  lib.sh:6:# lib.sh — shared helpers for the #442 observation scripts.
  lib.sh:47:    case "$a" in
  lib.sh:48:      *[Ss]uper[Cc]laude-[Oo]rg*|*superclaude-org*)
coupled sites: lib.sh:44-53 (the whole gh_fork argument loop is the rule being fixed).
after:
  lib.sh:46-49: loop now lowercases each argument with tr and matches *superclaude-org* on the lowercased copy (verified: SUPERCLAUDE-ORG/x, SuperClaude-ORG/x, sUPERCLAUDE-ORG/x refused, stub not reached).

## family: timeout-bound
defect form: external calls (gh, git, bash sub-invocations) not wrapped in `timeout`, required by the plan Constraints for every script.
search command: grep -n -e 'command gh' -e 'git worktree' -e 'command ' .dev/issues/442/scripts/lib.sh .dev/issues/442/scripts/selftest.sh .dev/issues/442/scripts/lib-selftest.sh
before-output (touched files):
  lib.sh:71:  command gh "$@"
  lib.sh:76:  git worktree list --porcelain | awk ...
  selftest.sh:46: bash "$here/lib-selftest.sh" || fail lib "lib-selftest exited $?"
coupled sites: lib.sh:70-71 (gh_fork exec), lib.sh:74-77 (main_checkout), selftest.sh:46 (the one sub-invocation selftest.sh makes).
after:
  lib.sh: gh_fork runs `command timeout "${OB_TIMEOUT_S:-60}" gh "$@"`; main_checkout wraps `git worktree list` the same way.
  selftest.sh:46: now `timeout 60 bash "$here/lib-selftest.sh"`.
