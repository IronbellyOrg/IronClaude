#!/usr/bin/env bash
# H3 base check: .dev/reflect absent in all three base tarballs, and the repaired lines named in MR T3(a) absent from
# the base of the package whose plan they mask: the line at that number in today's checkout must not occur anywhere in
# that base's copy of the file (a file missing from the base counts as absent and is printed as MISSING-FILE).
# Deviation from DESIGN 6.3: refs/tiers.md:42 (B8) is checked in the alias base, not the designSpec base, because the
# alias ground truth names tiers.md and the alias squash commit 4eb75698d is the commit that edits it.
set -u -o pipefail
. "$(dirname "$0")/_spike.sh"
OUTD=$SPIKES/out/h3; mkdir -p "$OUTD"; LOG=$OUTD/h3.log; : > "$LOG"
V=PASS
for PKG in $(jq -r '.packages[]' "$PANELS"); do
  bash "$R2_HOME/bin/build-sandbox.sh" "$PKG" >/dev/null || { V=FAIL; echo "build failed $PKG" >> "$LOG"; continue; }
  if tar -tf "$SBR/base/$PKG.tar" | grep -q '\.dev/reflect'; then V=FAIL; echo "LEAK .dev/reflect in $PKG" >> "$LOG"
  else echo "OK no .dev/reflect in $PKG" >> "$LOG"; fi
done
DS=TASK-WF-designSpec-20261107-075614; AL=TASK-WF-makeTheAliasOnly-20261105-051649
for spec in $DS:src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md:146 $DS:src/superclaude/pr_submit/merge_guard.py:256 \
            $DS:src/superclaude/commands/pr-submit.md:81 $AL:src/superclaude/skills/sc-issue-protocol/refs/tiers.md:42; do
  pkg=${spec%%:*}; rest=${spec#*:}; f=${rest%:*}; n=${rest##*:}
  today=$(sed -n "${n}p" "$REPO/$f")
  if base=$(tar -xOf "$SBR/base/$pkg.tar" "./$f" 2>/dev/null); then note=""; else base=""; note=" MISSING-FILE"; fi
  if [ -z "$(tr -d '[:space:]' <<<"$today")" ]; then V=FAIL; echo "BLANK today $rest" >> "$LOG"; continue; fi
  if grep -qxF -- "$today" <<<"$base"; then V=FAIL; res=PRESENT; else res=ABSENT; fi
  printf '%s%s %s base=%s today=%q base_line=%q\n' "$res" "$note" "$rest" "$pkg" "$today" "$(sed -n "${n}p" <<<"$base")" >> "$LOG"
done
cat "$LOG"
record H3 "$V" "$LOG" "$(grep -c '^ABSENT' "$LOG")/4 masked lines absent from their package's base ($(grep -c 'MISSING-FILE' "$LOG") because the file does not exist there yet); .dev/reflect absent $(grep -c '^OK no' "$LOG")/3"
[ "$V" = PASS ]
