#!/usr/bin/env bash
# Task 9 final scope check against the Task 1 baseline. Run from the worktree root: bash <this file>
# Prints each step as it runs; the caller saves the output as ./artifacts/t9-scope.log.
set -u
PKG=.dev/tasks/to-do/TASK-WF-specR1-20261023-031725
A=$PKG/artifacts
H=$(cat $A/t1-head.txt)
fail=0
ok()  { echo "PASS $1"; }
bad() { echo "FAIL $1"; fail=1; }

echo '== 1. scripts/README.md publish-pypi.yml mentions'
echo "\$ grep -c 'publish-pypi.yml' scripts/README.md"
n=$(grep -c 'publish-pypi.yml' scripts/README.md); echo "$n"
if [ "$n" = 0 ]; then ok "0 mentions"; elif [ "$n" = 1 ] && grep 'publish-pypi.yml' scripts/README.md | grep -q 'was removed'; then
  echo "\$ grep -n 'publish-pypi.yml' scripts/README.md"; grep -n 'publish-pypi.yml' scripts/README.md; ok "1 mention and that line says the workflow was removed"
else bad "publish-pypi.yml mention count/wording"; fi
echo "\$ grep -n 'git+https://github.com/IronbellyOrg/IronClaude' scripts/README.md"
grep -n 'git+https://github.com/IronbellyOrg/IronClaude' scripts/README.md && ok "new text contains git+https://github.com/IronbellyOrg/IronClaude" || bad "git+https URL missing"

echo; echo '== 2. scripts/README.md diff against the Task 1 baseline (saved to ./artifacts/t9-scripts-readme.diff)'
echo "\$ diff <(git show \$(cat ./artifacts/t1-head.txt):scripts/README.md) scripts/README.md > ./artifacts/t9-scripts-readme.diff"
git show "$H:scripts/README.md" > /tmp/t9-base-scripts-README.md
diff /tmp/t9-base-scripts-README.md scripts/README.md > $A/t9-scripts-readme.diff; echo "rc=$? (1 = files differ)"
cat $A/t9-scripts-readme.diff
echo "hunk headers (left side = base line range):"
grep -E '^[0-9]+(,[0-9]+)?[acd][0-9]+(,[0-9]+)?$' $A/t9-scripts-readme.diff
outside=$(grep -E '^[0-9]+(,[0-9]+)?[acd]' $A/t9-scripts-readme.diff | sed -E 's/[acd].*//' | awk -F, '{s=$1; e=($2==""?$1:$2); if (s<7 || e>12) print $0}')
[ -z "$outside" ] && ok "all changes are inside old lines 7-12" || bad "changes outside old lines 7-12: $outside"

echo; echo '== 3. hashes of every baseline-hashed path (saved to ./artifacts/t9-hashes-after.txt)'
echo "\$ for each path in ./artifacts/t1-hashes-before.txt: sha256sum <path>, or 'MISSING <path>' if it no longer exists"
: > $A/t9-hashes-after.txt
while IFS= read -r line; do
  case "$line" in MISSING\ *) p=${line#MISSING } ;; *) p=${line#*  } ;; esac
  if [ -e "$p" ] || [ -L "$p" ]; then sha256sum -- "$p" >> $A/t9-hashes-after.txt; else echo "MISSING $p" >> $A/t9-hashes-after.txt; fi
done < $A/t1-hashes-before.txt
echo "lines: before=$(wc -l < $A/t1-hashes-before.txt) after=$(wc -l < $A/t9-hashes-after.txt)"
echo "\$ cmp ./artifacts/t1-hashes-before.txt ./artifacts/t9-hashes-after.txt"
cmp $A/t1-hashes-before.txt $A/t9-hashes-after.txt; rc=$?; echo "rc=$rc"
[ $rc -eq 0 ] && ok "cmp exits 0: no baseline-hashed file changed" || bad "cmp non-zero"

echo; echo '== 4. status after (saved to ./artifacts/t9-status-after.txt) versus ./artifacts/t1-status-before.txt'
echo '$ git status --porcelain -uall -z | tr "\0" "\n"   # saved to artifacts/t9-status-after.txt'
git status --porcelain -uall -z | tr '\0' '\n' > $A/t9-status-after.txt
echo "lines: before=$(wc -l < $A/t1-status-before.txt) after=$(wc -l < $A/t9-status-after.txt)"
echo '$ comm -13 <(sort ./artifacts/t1-status-before.txt) <(sort ./artifacts/t9-status-after.txt)   # entries new since the baseline'
comm -13 <(sort $A/t1-status-before.txt) <(sort $A/t9-status-after.txt) > /tmp/t9-new-entries.txt
cat /tmp/t9-new-entries.txt
echo '$ comm -23 <(sort ./artifacts/t1-status-before.txt) <(sort ./artifacts/t9-status-after.txt)   # baseline entries that disappeared'
comm -23 <(sort $A/t1-status-before.txt) <(sort $A/t9-status-after.txt) > /tmp/t9-gone-entries.txt
cat /tmp/t9-gone-entries.txt
[ -s /tmp/t9-gone-entries.txt ] && bad "baseline entries disappeared" || ok "no baseline entry disappeared"
echo; echo 'Classification of the new entries:'
tooling=(); badpaths=()
while IFS= read -r e; do
  [ -n "$e" ] || continue
  p=${e:3}
  case "$p" in
    .github/workflows/*|scripts/README.md|$PKG/*) echo "allowed         $e" ;;
    .dev/reflect/*|.dev/troubleshoot/*|.dev/workflow/*) echo "tooling output  $e"; tooling+=("$e") ;;
    *) echo "NOT ALLOWED     $e"; badpaths+=("$e") ;;
  esac
done < /tmp/t9-new-entries.txt
echo; echo '### Tooling output'
if [ ${#tooling[@]} -eq 0 ]; then echo '(none)'; else printf '%s\n' "${tooling[@]}"; fi
[ ${#badpaths[@]} -eq 0 ] && ok "every new entry is under .github/workflows/, is scripts/README.md, is under this package, or is tooling output" || bad "paths outside the allowed roots: ${badpaths[*]}"

echo; echo '== 5. positive checks'
echo '$ git status --porcelain -- .github/workflows/pull-sync-framework.yml .github/workflows/boundary-guard.yml .github/workflows/test.yml .github/workflows/README.md scripts/README.md'
git status --porcelain -- .github/workflows/pull-sync-framework.yml .github/workflows/boundary-guard.yml .github/workflows/test.yml .github/workflows/README.md scripts/README.md | tee /tmp/t9-pos.txt
[ "$(grep -c '^ M ' /tmp/t9-pos.txt)" = 5 ] && [ "$(wc -l < /tmp/t9-pos.txt)" = 5 ] && ok "all five files are listed as modified" || bad "expected five modified files"
echo '$ git status --porcelain -- src tests Makefile pyproject.toml .claude'
git status --porcelain -- src tests Makefile pyproject.toml .claude | tee /tmp/t9-neg.txt
extra=$(sort /tmp/t9-neg.txt | comm -13 <(sort $A/t1-status-before.txt) -)
[ -z "$extra" ] && ok "nothing under src, tests, Makefile, pyproject.toml, .claude that is not in the baseline" || bad "new entries under protected paths: $extra"

echo; [ $fail -eq 0 ] && echo 'RESULT ALL PASS' || echo 'RESULT FAIL'
exit $fail
