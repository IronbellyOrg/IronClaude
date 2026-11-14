#!/usr/bin/env bash
# Verify pins.json (R-02, R-07, R-29, R-30, D10); one line per pin; exit 1 on any mismatch.
# usage: pins-check.sh            check
#        pins-check.sh --write    (re)write pins.json from the current files (run once after editing config)
set -u -o pipefail
R5=$(cd "$(dirname "$0")/.." && pwd); CFG=${R5_CONFIG:-$R5/config}
EVAL=${R5_EVAL:-$(cd "$R5/../../20261111-a1" && pwd)}
PINS=${R5_PINS:-$CFG/pins.json}
REPO=$(git -C "$R5" rev-parse --show-toplevel)
sum() { sha256sum "$1" 2>/dev/null | cut -d' ' -f1; }
if [ "${1:-}" = --write ]; then
  INST=$(dirname "$(dirname "$(readlink -f "$(command -v superclaude)")")")
  IP=$(ls -d "$INST"/lib/python3*/site-packages/superclaude/cli/review | head -1)
  FILES=$(cd "$CFG" && for f in catalogue.md surface.regex templates/*.txt; do printf '%s\t%s\n' "$f" "$(sum "$f")"; done | jq -R 'split("\t")|{(.[0]):.[1]}' | jq -s add)
  PARSER=$(jq -n --arg wf "$REPO/src/superclaude/cli/review/findings.py" --arg wl "$REPO/src/superclaude/cli/review/ledger.py" \
    --arg if_ "$IP/findings.py" --arg il "$IP/ledger.py" \
    '{worktree_findings:$wf,worktree_ledger:$wl,installed_findings:$if_,installed_ledger:$il}')
  PARSER=$(jq --arg a "$(sum "$REPO/src/superclaude/cli/review/findings.py")" --arg b "$(sum "$REPO/src/superclaude/cli/review/ledger.py")" \
    '. + {findings_sha256:$a, ledger_sha256:$b}' <<<"$PARSER")
  jq -n --arg j "$(sum "$EVAL/tools/tmp-scripts/judge-one.sh")" --argjson f "$FILES" --argjson p "$PARSER" \
    '{judge_one_sha256:$j,config_files:$f,parser:$p}' > "$PINS"
  echo "wrote $PINS"; exit 0
fi
bad=0
chk() { if [ "$2" = "$3" ] && [ -n "$2" ]; then echo "OK   $1"; else echo "FAIL $1 have=$3 want=$2"; bad=1; fi; }
chk judge-one.sh "$(jq -r .judge_one_sha256 "$PINS")" "$(sum "$EVAL/tools/tmp-scripts/judge-one.sh")"
while IFS=$'\t' read -r f h; do chk "config/$f" "$h" "$(sum "$CFG/$f")"; done < <(jq -r '.config_files|to_entries[]|"\(.key)\t\(.value)"' "$PINS")
for kind in findings ledger; do
  W=$(jq -r ".parser.worktree_$kind" "$PINS"); I=$(jq -r ".parser.installed_$kind" "$PINS"); P=$(jq -r ".parser.${kind}_sha256" "$PINS")
  chk "worktree $kind.py" "$P" "$(sum "$W")"; chk "installed $kind.py (D10)" "$P" "$(sum "$I")"
done
for s in "$CFG"/values*/*/SHA256SUMS; do  # values/ and values-slack<S>/ (owner decision 2026-11-14)
  [ -f "$s" ] || continue
  lbl="$(basename "$(dirname "$(dirname "$s")")")/$(basename "$(dirname "$s")")"
  if (cd "$(dirname "$s")" && sha256sum -c --quiet SHA256SUMS >/dev/null 2>&1); then echo "OK   $lbl"; else echo "FAIL $lbl"; vbad=1; fi
done
if (cd "$REPO" && PYTHONPATH="$R5/lib" uv run --no-sync python -m r5.audit static >/dev/null); then echo "OK   audit static"; else echo "FAIL audit static"; bad=1; fi
# exit 3 = only a values sum failed (launch.sh reports that per panel as "F6 not runnable", exit 3, R-30)
[ $bad = 1 ] && exit 1; [ "${vbad:-0}" = 1 ] && exit 3; exit 0
