#!/usr/bin/env bash
# lib-selftest.sh — Task 1 cases for lib.sh, run by selftest.sh.
set -u -o pipefail
umask 077

here=$(cd -- "$(dirname -- "$0")" && pwd)
failures=0
ck() { if [ "$2" = "$3" ]; then printf 'OK %s\n' "$1"; else printf 'FAIL %s got=<%s> want=<%s>\n' "$1" "$2" "$3"; failures=$((failures+1)); fi; }

# 1. bash -n on lib.sh
if bash -n "$here/lib.sh"; then ck lib-bash-n ok ok; else ck lib-bash-n fail ok; fi

# Isolated OB root for these cases.
T=$(mktemp -d /tmp/ob-lib.XXXXXXXX)
export OB=$T
# shellcheck source=lib.sh
source "$here/lib.sh"

# 2. gh_fork pins --repo on a normal subcommand and the stub receives it.
mkdir -p "$T/stublog"; export OB_STUB_LOG=$T/stublog
out=$(gh_fork issue list)
grep -q -- '--repo IronbellyOrg/IronClaude' "$T/stublog/gh.log" \
  && ck gh-fork-repo ok ok || ck gh-fork-repo missing ok

# 2b. `gh repo view` has no --repo flag: the positional repository goes through, and nothing is appended.
rm -f "$T/stublog/gh.log"
gh_fork repo view IronbellyOrg/IronClaude --json nameWithOwner >/dev/null
ck gh-fork-repo-view "$(cat "$T/stublog/gh.log")" 'repo view IronbellyOrg/IronClaude --json nameWithOwner'
rm -f "$T/stublog/gh.log"
if gh_fork repo view SuperClaude-Org/SuperClaude_Framework 2>/dev/null; then ck gh-fork-repo-view-refuse called ok; else ck gh-fork-repo-view-refuse ok ok; fi
# every other `gh repo` form is refused before gh runs: no argument, another repository, another verb
for form in "repo view" "repo view someone/else" "repo delete IronbellyOrg/IronClaude"; do
  # shellcheck disable=SC2086
  if gh_fork $form 2>/dev/null || [ -e "$T/stublog/gh.log" ]; then ck "gh-fork-repo-refuse:$form" called ok; else ck "gh-fork-repo-refuse:$form" ok ok; fi
  rm -f "$T/stublog/gh.log"
done

# 3. gh_fork api refuses a path outside the fork, in every casing.
rm -f "$T/stublog/gh.log"
if gh_fork api repos/SuperClaude-Org/x 2>/dev/null; then
  ck gh-fork-refuse called ok
else
  if [ -e "$T/stublog/gh.log" ]; then ck gh-fork-refuse reached-stub ok; else ck gh-fork-refuse ok ok; fi
fi
rm -f "$T/stublog/gh.log"
for slug in SUPERCLAUDE-ORG/x SuperClaude-ORG/x sUPERCLAUDE-ORG/x; do
  if gh_fork issue view "$slug" 2>/dev/null; then
    ck "gh-fork-refuse-case:$slug" called ok
  elif [ -e "$T/stublog/gh.log" ]; then
    ck "gh-fork-refuse-case:$slug" reached-stub ok
  else
    ck "gh-fork-refuse-case:$slug" ok ok
  fi
  rm -f "$T/stublog/gh.log"
done

# 4. state file round-trip, including a value with spaces, no eval.
state_set T1 421
state_set WT_T1 "$T/wt one"
state_set PR_URL "https://github.com/IronbellyOrg/IronClaude/pull/9"
ck state-get-num "$(state_get T1)" 421
ck state-get-spaces "$(state_get WT_T1)" "$T/wt one"
ck state-get-url "$(state_get PR_URL)" "https://github.com/IronbellyOrg/IronClaude/pull/9"
if state_get ABSENT >/dev/null 2>&1; then ck state-get-absent found missing; else ck state-get-absent ok ok; fi

# 5. step output shape.
ck step-shape "$(step s1 OK | tr '\n' '|')" "BEGIN s1|OK s1|"

exit $failures
