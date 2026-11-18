#!/usr/bin/env bash
# Stage 0 inventory freeze (Task 1). Re-run from the repository root:
#   bash .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/artifacts/stage0-inventory-freeze.sh
# Plain grep only (the Grep tool skips gitignored folders, so it would miss the project .claude/ copies).
# Output: stage0-inventory-freeze.md in this folder (overwritten each run).
set -u -o pipefail
A=.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/artifacts
OUT=$A/stage0-inventory-freeze.md
TBL=$(mktemp); HITS=$(mktemp); CMDS=$(mktemp); DIFFS=$(mktemp)
trap 'rm -f "$TBL" "$HITS" "$CMDS" "$DIFFS"' EXIT
SRC=src/superclaude; PLG=plugins/superclaude; CLD=.claude
FAILSCOPE="src/superclaude/agents src/superclaude/skills src/superclaude/templates src/superclaude/rules"
n=0
# row <id> <label> <scope-label> <spec-files|-> <spec-lines|-> <grep-opts> <pattern> <paths...>
row() {
  local id=$1 label=$2 scope=$3 sf=$4 sl=$5 opts=$6 pat=$7; shift 7
  local out files lines df dl
  n=$((n+1))
  out=$(grep -rnIH $opts -e "$pat" -- "$@" 2>/dev/null)
  if [ -z "$out" ]; then files=0; lines=0; else files=$(printf '%s\n' "$out" | cut -d: -f1 | sort -u | wc -l); lines=$(printf '%s\n' "$out" | wc -l); fi
  if [ "$sf" = "-" ]; then df="n/a"; else df=$((files-sf)); fi
  if [ "$sl" = "-" ]; then dl="n/a"; else dl=$((lines-sl)); fi
  local spec="" diff=""
  [ "$sf" != "-" ] && spec="${sf} files"
  [ "$sl" != "-" ] && spec="${spec:+$spec / }${sl} lines"
  [ -z "$spec" ] && spec="not stated"
  diff="files ${df}, lines ${dl}"
  printf '| %s | %s | `%s` | %s | %s files / %s lines | %s |\n' "$id" "$label" "$scope" "$spec" "$files" "$lines" "$diff" >> "$TBL"
  printf "grep -rnIH %s -e '%s' -- %s\n" "$opts" "${pat//\'/\'\\\'\'}" "$*" >> "$CMDS"
  if [ "$df" != "0" ] && [ "$df" != "n/a" ] || { [ "$dl" != "0" ] && [ "$dl" != "n/a" ]; }; then
    printf -- '- [%s] %s in `%s`: spec %s, observed %s files / %s lines\n' "$id" "$label" "$scope" "$spec" "$files" "$lines" >> "$DIFFS"
  fi
  { printf '\n### [%s] %s, scope `%s` (%s files, %s lines)\n\n' "$id" "$label" "$scope" "$files" "$lines"
    if [ -n "$out" ]; then printf '```text\n%s\n```\n' "$out"; else printf 'no hits\n'; fi; } >> "$HITS"
}

# P1..P8 over the three scopes
for S in "$SRC" "$PLG" "$CLD"; do
  case $S in "$SRC") s1="11 11"; s2="11 11"; s3="11 -"; s4="12 -"; s5="7 -"; s6="3 7"; s7="22 120";;
             "$PLG") s1="0 -"; s2="- -"; s3="- -"; s4="- -"; s5="- -"; s6="- -"; s7="- -";;
             "$CLD") s1="6 -"; s2="- -"; s3="- -"; s4="- -"; s5="- -"; s6="- -"; s7="- -";; esac
  row P1 'definition sentence S1' "$S" $s1 -F 'Grade every review finding as blocking or minor' "$S"
  row P2 '"Blocking is a real defect" (both cases)' "$S" $s2 -i 'Blocking is a real defect' "$S"
  row P3 'S2 "Minor findings never fail a review"' "$S" $s3 -F 'Minor findings never fail a review' "$S"
  row P4 'S3 cap "at most 2 fix cycles (3 reviews)"' "$S" $s4 -E 'at most 2 fix cycles \(3 reviews\)' "$S"
  row P5 'S5 "CRITICAL and IMPORTANT findings are blocking"' "$S" $s5 -F 'CRITICAL and IMPORTANT findings are blocking' "$S"
  row P6 '"follow-up candidates"' "$S" $s6 -F 'follow-up candidates' "$S"
  row P7 '"2 fix cycles"' "$S" $s7 -F '2 fix cycles' "$S"
done
# P8 merge-rule patterns of spec 10.3 (case-insensitive). Spec: 13 lines in 10 files in the change list; 4 further
# sites are listed as not changed (sc-auggie-review-protocol:228, remediate_parser.py x3 lines) so raw counts exceed 13.
for S in "$SRC" "$PLG" "$CLD"; do
  case $S in "$PLG") m="0 0";; *) m="- -";; esac
  row P8a 'merge rule, first pattern' "$S" $m -iE 'highest severity|more severe' "$S"
  row P8b 'merge rule, second pattern' "$S" $m -iE 'higher severity|max(imum)? severity|worst (severity|rating)|highest (rating|grade)' "$S"
done
# P8 union over src (spec 10.3 change list: 13 lines in 10 files; the spec also names further sites it leaves unchanged)
row P8u 'merge rule, both patterns combined (spec 10.3 change list: 13 lines / 10 files, which excludes the sites the spec leaves unchanged)' "$SRC" 10 13 -iE 'highest severity|more severe|higher severity|max(imum)? severity|worst (severity|rating)|highest (rating|grade)' "$SRC"
# P9 tasklist
row P9 'tasklist "High or Medium" / "Medium (blocking)"' "src/superclaude/skills/sc-tasklist-protocol/SKILL.md" - 7 -E 'High or Medium|Medium \(blocking\)' src/superclaude/skills/sc-tasklist-protocol/SKILL.md
# P10 fixed FAIL triggers (REQ-30) plus the extra pattern; spec states no counts
row F1 'FAIL trigger "= FAIL"' "$FAILSCOPE" - - -F '= FAIL' $FAILSCOPE
row F2 "FAIL trigger \"that's a FAIL\"" "$FAILSCOPE" - - -F "that's a FAIL" $FAILSCOPE
row F3 'FAIL trigger "regardless of severity"' "$FAILSCOPE" - - -F 'regardless of severity' $FAILSCOPE
row F4 'FAIL trigger "highest severity"' "$FAILSCOPE" - - -F 'highest severity' $FAILSCOPE
row F5 'FAIL trigger "never minor"' "$FAILSCOPE" - - -F 'never minor' $FAILSCOPE
row F6 'FAIL trigger "always IMPORTANT"' "$FAILSCOPE" - - -F 'always IMPORTANT' $FAILSCOPE
row F7 'extra pattern "Any CRITICAL or IMPORTANT issue exists" (first-plan review: 8 lines rf-qa-qualitative, 1 agent_template_qa)' "$FAILSCOPE" - - -F 'Any CRITICAL or IMPORTANT issue exists' $FAILSCOPE

{
  printf '# Stage 0: frozen pattern inventory (spec section 10)\n\n'
  printf 'Generated: %s by `%s/stage0-inventory-freeze.sh` (re-run from the repository root). HEAD: %s.\n\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$A" "$(git rev-parse --short HEAD)"
  printf 'Method: plain `grep -rnI` (not the Grep tool, which skips gitignored folders and so misses the project `.claude/` copies). Case-sensitive unless the command shows `-i`. "Observed" counts matching lines and distinct files. Spec counts are those stated in spec section 10 (`n/a` difference where the spec states no count; the spec counts apply to the `src/superclaude` scope except where its own text names another).\n\n'
  printf '## Table\n\n| ID | Pattern | Scope | Spec count | Observed count | Difference |\n|---|---|---|---|---|---|\n'
  cat "$TBL"
  printf '\n## Differences from the spec\n\n'
  if [ -s "$DIFFS" ]; then
    printf 'Rows whose observed count differs from a stated spec count:\n\n'; cat "$DIFFS"
  else printf 'No pattern differs from a stated spec count.\n'; fi
  printf '\nReading of row P8u (written by hand after reading every hit at HEAD %s; the numbers above are from the run, this reading is not recomputed): the 13 lines in 10 files of the spec section 10.3 change list are all present and unchanged (task/SKILL.md 252 and 361; rf-qa 83; rf-qa-qualitative 84; rf-analyst 75; tech-reference 510 and 513; readme 542 and 547; tdd build-request-template 122; operational-guide 511; agent_template_qa 85; agent_template_analysis 466). The 10 further lines in 5 files are sites the spec does not put in that list: remediate_parser.py 55, 301, 365 and sc-auggie-review-protocol/SKILL.md 228 (the spec names these as not changed), fmea_classifier.py 45, 304, 310, 323 and severity_router.py 21 (the spec says these rank unrelated things), and sc-pr-submit-protocol/refs/severity-routing.md 65 (clamping to a category ceiling; not named in the spec, not a label-max merge). So the spec count holds and the raw pattern count is larger by those 10 lines. Plugin tree: 0 matches, as the spec says.\n' "$(git rev-parse --short HEAD)"
  printf '\n## Commands used\n\nRun from the repository root, in this order:\n\n```bash\n'
  cat "$CMDS"
  printf '```\n\n## Hit lines (file:line:text)\n\nThe fixed FAIL-trigger hits (F1 to F7, including `Any CRITICAL or IMPORTANT issue exists`) are the list later tasks use; they come first.\n'
  # fixed FAIL triggers first, then the rest
  awk 'BEGIN{RS="\n### ";ORS=""} NR==1{next} /^\[F[0-9]\]/{print "\n### " $0}' "$HITS"
  printf '\n## Hit lines of the definition, cap, merge and tasklist patterns\n'
  awk 'BEGIN{RS="\n### ";ORS=""} NR==1{next} /^\[(P[0-9])/{print "\n### " $0}' "$HITS"
} > "$OUT"
echo "wrote $OUT"
