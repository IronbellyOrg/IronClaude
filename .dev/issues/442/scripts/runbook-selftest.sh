#!/usr/bin/env bash
# runbook-selftest.sh — Task 9 cases, run by selftest.sh.
# The runbook wording the scripted path changed, section 6 against the scripts folder,
# every quoted script fragment against the script line it cites, and the fixed line
# anchors that other self-tests read.
set -u -o pipefail
umask 077

here=$(cd -- "$(dirname -- "$0")" && pwd)
RB=$(cd -- "$here/.." && pwd)/observation-runbook.md
failures=0
ck() { if [ "$2" = "$3" ]; then printf 'OK %s\n' "$1"; else printf 'FAIL %s got=<%s> want=<%s>\n' "$1" "$2" "$3"; failures=$((failures+1)); fi; }

# 1. the old wording is gone, and the new statements are there (the last two fail on the old text)
ck old-not-representative "$(grep -c 'not representative' "$RB" || true)" 0
ck old-typed-by-a-person "$(grep -c 'must be.*typed by a person' "$RB" || true)" 0
ck new-orca-terminal-send "$([ "$(grep -c 'orca terminal send' "$RB")" -ge 1 ] && echo yes)" yes
ck new-authorization "$(grep -c 'Owner authorization of 2026-11-08' "$RB" || true)" 1

# 2. section 6 names every script file in the folder, and names no file that is missing
sec=$(sed -n '/^## 6\. Scripted path/,/^## Appendix/p' "$RB")
ck sec6-present "$([ -n "$sec" ] && echo yes)" yes
missing=""
for f in "$here"/*.sh; do
  b=$(basename "$f")
  printf '%s\n' "$sec" | grep -qF "\`$b" || missing="$missing $b"
done
ck sec6-names-every-script "${missing:-none}" none
ghost=""
for b in $(printf '%s\n' "$sec" | grep -oE '`[a-z0-9-]+\.sh' | tr -d '`' | sort -u); do
  [ -f "$here/$b" ] || ghost="$ghost $b"
done
ck sec6-names-no-missing-script "${ghost:-none}" none
ck sec6-stops "$([ "$(printf '%s\n' "$sec" | grep -c 'NEEDS_INPUT\|BLOCKED login-isolated-home')" -ge 2 ] && echo yes)" yes
ck sec6-apply-rule "$([ "$(printf '%s\n' "$sec" | grep -c -- '--apply')" -ge 1 ] && echo yes)" yes

# 3. every quoted fragment is on the script line it cites (sections 4.2 and 6); a self-test is not citable
check_quotes() {  # check_quotes <runbook file>: FAIL lines, then PAIRS=<n> BAD=<n>
  local rbf=$1 text pair lit cites c f n line bad=0 pairs=0
  local -a arr
  text=$(sed -n '/^### 4\.2/,/^## 5\./p;/^## 6\. Scripted path/,/^## Appendix/p' "$rbf")
  while IFS= read -r pair; do
    pairs=$((pairs + 1))
    lit=${pair#\`}; lit=${lit%%\`*}
    cites=${pair##*\` (}; cites=${cites%)}
    IFS=',' read -ra arr <<< "$cites"
    for c in "${arr[@]}"; do
      c=${c# }; f=${c%%:*}; n=${c##*:}
      case "$f" in
        *-selftest.sh) printf 'FAIL quote %s: a self-test is not citable\n' "$c"; bad=$((bad + 1)); continue ;;
      esac
      line=$(sed -n "${n}p" "$here/$f" 2>/dev/null)
      case "$line" in
        *"$lit"*) ;;
        *) printf 'FAIL quote %s %s\n' "$c" "$lit"; bad=$((bad + 1)) ;;
      esac
    done
  done < <(printf '%s\n' "$text" | grep -oE '`[^`]+` \([a-z0-9-]+\.sh:[0-9]+(, [a-z0-9-]+\.sh:[0-9]+)*\)')
  printf 'PAIRS=%s BAD=%s\n' "$pairs" "$bad"
}
res=$(check_quotes "$RB")
ck quotes-all-on-cited-line "$(printf '%s\n' "$res" | grep -c '^FAIL')" 0
pairs=$(printf '%s\n' "$res" | sed -n 's/^PAIRS=\([0-9]*\) .*/\1/p')
ck quotes-enough-pairs "$([ "${pairs:-0}" -ge 6 ] && echo yes)" yes
# the check can fail: one changed quote character in a temporary copy of the runbook
tmp=$(mktemp)
sed 's/`NEEDS_INPUT` (driver.sh:58/`NEEDS_INPUTX` (driver.sh:58/' "$RB" > "$tmp"
mres=$(check_quotes "$tmp")
rm -f -- "${tmp:?}"
ck quotes-check-can-fail "$([ "$(printf '%s\n' "$mres" | grep -c '^FAIL')" -ge 1 ] && echo yes)" yes

# 4. every line of section 6 carries a script citation, except blank lines, headings, table header
#    and separator rows, and the file list line
uncited=$(printf '%s\n' "$sec" | awk '
  /^[[:space:]]*$/ { next }
  /^#/ { next }
  /^\|[-| ]+\|$/ { next }
  /^\| (Order|Literal printed) \|/ { next }
  /^Files not in the run order:/ { next }
  !/[a-z0-9-]+\.sh:[0-9]+/ { print NR ": " $0 }')
ck sec6-every-line-cited "${uncited:-none}" none

# 4b. the claim's terminal, layers and release come from launch-result.json, not from screen text or an Orca lookup (issue 691, Part B)
ck result-file-cited "$([ "$(grep -c 'launch-result.json' "$RB")" -ge 7 ] && echo yes)" yes
ck gov-no-terminal-list "$(grep -c 'terminal list' "$here/session-gov.sh" || true)" 0
ck rb-terminal-list-only-as-removed "$(grep 'orca terminal list' "$RB" | grep -vc 'no longer\|never' || true)" 0
ck gov-no-screen-parse "$(grep -c 'CLAIM_LAST\|CLAIM_TXT' "$here/session-gov.sh" || true)" 0

# 5. the line anchors other self-tests read (session A 228-472, filters 505-520, sessions B to E 536-697)
ck anchor-session-a "$(sed -n '228p' "$RB" | cut -c1-16)" '### 2.1 Session '
ck anchor-filters "$(sed -n '505p' "$RB" | cut -c1-5)" '# F1:'
ck anchor-filters-end "$(sed -n '520p' "$RB" | cut -c1-13)" "jq -sr '(map("
ck anchor-session-b "$(sed -n '536p' "$RB" | cut -c1-14)" '#### 2.2.1 Ses'
ck anchor-section-3 "$(sed -n '698p' "$RB" | cut -c1-5)" '## 3.'

exit $failures
