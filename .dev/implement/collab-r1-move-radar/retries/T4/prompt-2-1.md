397b62f0e95b6dad3c9c888d7928c60899f86a87
Review one task for spec compliance.

Task brief: T4 (source: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/DESIGN.md; task grouping in .dev/implement/collab-r1-move-radar/tasks.md). Covers DESIGN.md section 1.2 rows `tools/run-reviewer.sh`, `tools/h2_normalize.py`, `tools/values.py`, the behaviour of sections 2.6 (timing values, Spike 4 aggregation) and 2.7 (reviewer runner: H1-H4, command, model and block check, retry R-44, hang guard R-43, H2 R-02, outputs), section 4's R-05 check, the stub `claude` of section 6 (tests/fixtures/bin/claude), and the tests T-10 (cmd part), T-11, T-12, T-13, F-8 (runner part: kill timing and hang_kill; the slo_breach flag is written by collab_summary.py in a later task), F-9, F-10 (runner part; the package-level `invalid` and launch exit 1 are launch.sh, a later task) and F-13. Implementation notes: the runner reads HANG_MS, its role and T_report from runs/<row>/<pkg>/run.json (written by launch.sh in a later task); `values.py deadlines` is the helper launch.sh will call to compute T0-based deadlines (planning values and a 2.0 x planning B hang guard when no values file exists and collab is 0; refusal for collab 1).
T4.AC1: the three tools implement the behaviour of DESIGN.md sections 2.6 and 2.7 and the R-05 allowed-difference set of section 4.
T4.AC2: T-10 (cmd part), T-11, T-12, T-13, F-8 (runner part), F-9, F-10 (runner part) and F-13 exist as tests that check what DESIGN.md 6.1/6.2 lists for them and pass: `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests -q`.
Global constraints: Orchestrator constraints: Create and edit files ONLY under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/ (plus .dev/implement/collab-r1-move-radar/ and scratch under /tmp/evalsb-collab-r1/ and /tmp/collab-r1/). Do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder, or any other redesign's folder. Do not stage, commit or push. Use uv for all Python. Gateway model sessions only under flock /tmp/collab-gateway.lock; models muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7; Opus only as blind judge; never Qwen or glm; NOFALLBACK=1. No full panel runs. Design hard limits: DESIGN.md section 0 'Hard limits carried into every script'.
Start sha: 397b62f0e95b6dad3c9c888d7928c60899f86a87
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh
new file mode 100644
index 000000000..7dc3fc7f4
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh
@@ -0,0 +1,135 @@
+#!/usr/bin/env bash
+# run-reviewer.sh <row> <pkg> <rid> <model> <collab 0|1> <T0_MS> [--root R1] [--sb SB]
+# run-reviewer.sh --print-cmd <row> <pkg> <rid> <model> <collab 0|1> <T0_MS> [--root R1] [--sb SB]
+# R1's reviewer launcher (DESIGN.md section 2.7): H1 brief, H3/H4 sandbox cwd, hang guard, one isolated retry,
+# H2 normalise + at most one re-ask. No fallback model, ever. Reads runs/<row>/<pkg>/run.json (HANG_MS, role, T_report)
+# and, with collab 1, runs/<row>/<pkg>/settings/<rid>.json. Writes runs/<row>/<pkg>/reviews/<rid>.*.
+# Exit 0 = valid reviewer, 1 = INVALID, 2 = refused before running.
+set -u -o pipefail
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+TOOLS=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
+R1=$(dirname "$TOOLS")
+SB=/tmp/evalsb-collab-r1
+PRINT=0; [ "${1:-}" = --print-cmd ] && { PRINT=1; shift; }
+[ $# -ge 6 ] || { echo "usage: run-reviewer.sh [--print-cmd] <row> <pkg> <rid> <model> <collab 0|1> <T0_MS>" >&2; exit 2; }
+ROW=$1; PKG=$2; RID=$3; MODEL=$4; COLLAB=$5; T0=$6; shift 6
+while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
+case $COLLAB in 0|1) ;; *) echo "REFUSE collab must be 0 or 1" >&2; exit 2;; esac
+[ $PRINT = 1 ] || [ "${NOFALLBACK:-}" = 1 ] || { echo "REFUSE NOFALLBACK must be 1" >&2; exit 2; }
+D=$R1/runs/$ROW/$PKG; OUT=$D/reviews; RUNJ=$D/run.json
+[ -f "$RUNJ" ] || { echo "REFUSE no $RUNJ" >&2; exit 2; }
+HANG_MS=$(jq -r .HANG_MS "$RUNJ"); ROLE=$(jq -r --arg r "$RID" '.role[$r] // empty' "$RUNJ")
+TREP=$(jq -r --arg r "$ROLE" '.T_report[$r] // 0' "$RUNJ")
+[ -n "$ROLE" ] || { echo "REFUSE $RID has no role in run.json" >&2; exit 2; }
+CAND=$SB/cand/$PKG/candidate.md; SRC=$SB/cand/$PKG/source.md; CWD=$SB/$PKG/repo
+BRIEF=$(cat "$R1/config/brief.txt")
+BRIEF=${BRIEF//@@CAND@@/$CAND}; BRIEF=${BRIEF//@@SRC@@/$SRC}
+BRIEF=${BRIEF//@@SHA@@/$(sha256sum "$CAND" | cut -d' ' -f1)}; BRIEF=${BRIEF//@@SRCSHA@@/$(sha256sum "$SRC" | cut -d' ' -f1)}
+SETTINGS=""; [ "$COLLAB" = 1 ] && SETTINGS=$(cat "$D/settings/$RID.json")
+now() { date +%s%3N; }
+build_argv() { # build_argv <attempt> <hang_left_s>: attempt 1 carries --settings (collab 1); attempt 2 never does
+  A=(timeout --kill-after=5 "$2" claude -p --model "$MODEL" --output-format json --permission-mode bypassPermissions
+     --disallowedTools Edit Write NotebookEdit)
+  if [ "$1" = 1 ] && [ -n "$SETTINGS" ]; then A+=(--settings "$SETTINGS"); fi
+}
+if [ $PRINT = 1 ]; then
+  build_argv 1 $(( (HANG_MS - $(now)) / 1000 ))
+  printf '%s\n' "${A[@]}" | jq -R . | jq -s -c --arg cwd "$CWD" --arg stdin "$BRIEF" '{cwd:$cwd, argv:., stdin:$stdin}'
+  exit 0
+fi
+
+mkdir -p "$OUT"
+START_MS=$(now); SIDS=(); ARGVS=(); HANG=false; WALLS=(); TOKS=()
+sids_json() { if [ ${#SIDS[@]} -eq 0 ]; then echo '[]'; else printf '%s\n' "${SIDS[@]}" | jq -R . | jq -s -c .; fi; }
+partial_meta() { # session ids are written as soon as they are known (R-46, K-7)
+  jq -n -c --arg rid "$RID" --argjson s "$(sids_json)" --argjson st "$START_MS" '{reviewer_id:$rid, session_ids:$s, start_ms:$st, partial:true}' > "$OUT/$RID.meta.json"
+}
+partial_meta
+run_attempt() { # run_attempt <n>; returns 0 when model_ok && block_ok && no API error
+  local a=$1 left s rc w obs tok tokall apierr mok bok sid lo le
+  left=$(( (HANG_MS - $(now)) / 1000 ))
+  if [ "$left" -le 0 ]; then HANG=true; return 1; fi
+  build_argv "$a" "$left"
+  ARGVS+=("$(printf '%s\n' "${A[@]}" | jq -R . | jq -s -c .)")
+  s=$(now)
+  ( cd "$CWD" && "${A[@]}" <<<"$BRIEF" ) > "$OUT/$RID.attempt$a.json" 2> "$OUT/$RID.attempt$a.err"
+  rc=$?; w=$(( $(now) - s ))
+  { [ $rc = 124 ] || [ $rc = 137 ]; } && HANG=true
+  jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$OUT/$RID.attempt$a.json" > "$OUT/$RID.attempt$a.md" 2>/dev/null
+  obs=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$OUT/$RID.attempt$a.json" 2>/dev/null)
+  tok=$(jq '[.[]|select(.type=="result")|.usage.output_tokens]|.[0] // 0' "$OUT/$RID.attempt$a.json" 2>/dev/null)
+  tokall=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$OUT/$RID.attempt$a.json" 2>/dev/null)
+  sid=$(jq -r '[.[]|select(.type=="result")|.session_id]|.[0] // empty' "$OUT/$RID.attempt$a.json" 2>/dev/null)
+  [ -n "$sid" ] && { SIDS+=("$sid"); SID=$sid; partial_meta; }
+  apierr=false; grep -q 'API Error' "$OUT/$RID.attempt$a.md" 2>/dev/null && apierr=true
+  lo=$(echo "$obs" | tr 'A-Z' 'a-z'); le=$(echo "$MODEL" | tr 'A-Z' 'a-z')
+  mok=false; [ -n "$obs" ] && [ "$obs" != "<synthetic>" ] && { [ "$lo" = "$le" ] || [ "$lo" = "$le-build" ]; } && mok=true
+  bok=false; grep -q '^```findings-v1' "$OUT/$RID.attempt$a.md" 2>/dev/null && bok=true
+  WALLS+=("$w"); TOKS+=("${tokall:-0}")
+  jq -n --arg rid "$RID" --arg exp "$MODEL" --arg obs "$obs" --argjson mok $mok --argjson bok $bok --argjson att "$a" \
+    --argjson w "$(( w / 1000 ))" --argjson wms "$w" --argjson tok "${tok:-0}" --argjson tokall "${tokall:-0}" --argjson rc "$rc" \
+    --argjson api $apierr --arg sid "$sid" \
+    '{reviewer_id:$rid,expected_model:$exp,observed_model:$obs,model_ok:$mok,findings_block:$bok,attempt:$att,wall_s:$w,
+      wall_ms:$wms,output_tokens_main:$tok,output_tokens_all:$tokall,exit:$rc,api_error:$api,session_id:$sid}' > "$OUT/$RID.attempt$a.meta.json"
+  $mok && $bok && ! $apierr
+}
+
+SID=""; OK=false; ATT=1; RETRY_S=null; ISO=false
+run_attempt 1 && OK=true
+if ! $OK && [ $(( HANG_MS - $(now) )) -ge 30000 ]; then  # R-44: one isolated retry, same model, no --settings
+  ATT=2; [ "$COLLAB" = 1 ] && ISO=true
+  s=$(now); run_attempt 2 && OK=true; RETRY_S=$(jq -n "($(now) - $s) / 1000")
+fi
+
+# H2 (R-02): normalise; at most one re-ask on the same session when the block still has parser errors
+DROPPED=0; REASK_S=null; REASK_TOK=0; REASK_MS=0
+h2() { (cd "$REPO" && uv run python "$TOOLS/h2_normalize.py" "$1" "$2" "$3") >/dev/null 2>&1; }
+if $OK; then
+  h2 "$OUT/$RID.attempt$ATT.md" "$OUT/$RID.norm.md" "$OUT/$RID.h2.json"
+  if [ "$(jq -r .ok "$OUT/$RID.h2.json")" != true ] && [ -n "$SID" ] \
+     && [ $(( HANG_MS - $(now) )) -ge "$(jq -n "1000 * (6 + $TREP) | floor")" ]; then
+    ERRS=$(jq -r '.errors[] | "line \(.line): \(.msg)"' "$OUT/$RID.h2.json")
+    PROMPT="Your findings-v1 block has these parser errors:
+$ERRS
+Reply with the complete corrected report, ending with the ## Findings block and the final verdict line."
+    left=$(( (HANG_MS - $(now)) / 1000 ))
+    R=(timeout --kill-after=5 "$left" claude -p --resume "$SID" --model "$MODEL" --output-format stream-json --verbose
+       --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit)
+    ARGVS+=("$(printf '%s\n' "${R[@]}" | jq -R . | jq -s -c .)")
+    s=$(now)
+    ( cd "$CWD" && "${R[@]}" <<<"$PROMPT" ) > "$OUT/$RID.reask.json" 2> "$OUT/$RID.reask.err"
+    rc=$?; REASK_MS=$(( $(now) - s )); REASK_S=$(jq -n "$REASK_MS / 1000")
+    { [ $rc = 124 ] || [ $rc = 137 ]; } && HANG=true
+    jq -s -r '[.[]|select(.type=="result")|.result][0] // ""' "$OUT/$RID.reask.json" > "$OUT/$RID.reask.md" 2>/dev/null
+    REASK_TOK=$(jq -s '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$OUT/$RID.reask.json" 2>/dev/null || echo 0)
+    rsid=$(jq -s -r '[.[]|select(.type=="result")|.session_id][0] // empty' "$OUT/$RID.reask.json" 2>/dev/null)
+    [ -n "$rsid" ] && [ "$rsid" != "$SID" ] && { SIDS+=("$rsid"); partial_meta; }
+    if [ -s "$OUT/$RID.reask.md" ]; then
+      h2 "$OUT/$RID.reask.md" "$OUT/$RID.norm2.md" "$OUT/$RID.h2-reask.json"
+      # the re-ask answer replaces the first report unless the merge would keep fewer of its lines
+      # (more kept lines wins; on a tie, fewer dropped lines wins)
+      if jq -e -n --slurpfile a "$OUT/$RID.h2-reask.json" --slurpfile b "$OUT/$RID.h2.json" \
+           '[$a[0].kept_lines, -$a[0].dropped_lines] >= [$b[0].kept_lines, -$b[0].dropped_lines]' >/dev/null; then
+        mv "$OUT/$RID.norm2.md" "$OUT/$RID.norm.md"; cp "$OUT/$RID.h2-reask.json" "$OUT/$RID.h2.json"
+      fi
+    fi
+  fi
+  DROPPED=$(jq '.dropped_lines' "$OUT/$RID.h2.json")  # block lines the merge parser will not keep
+  cp "$OUT/$RID.norm.md" "$OUT/$RID.md"
+else
+  cp "$OUT/$RID.attempt$ATT.md" "$OUT/$RID.md" 2>/dev/null || : > "$OUT/$RID.md"
+fi
+
+END_MS=$(now)
+LAST=$OUT/$RID.attempt$ATT.meta.json
+[ -f "$LAST" ] || jq -n --arg rid "$RID" --arg exp "$MODEL" '{reviewer_id:$rid,expected_model:$exp,observed_model:"",model_ok:false,findings_block:false,attempt:0,exit:124}' > "$LAST"
+ARGV_JSON=$(if [ ${#ARGVS[@]} -eq 0 ]; then echo '[]'; else printf '%s\n' "${ARGVS[@]}" | jq -s -c .; fi)
+jq --argjson s "$(sids_json)" --argjson st "$START_MS" --argjson en "$END_MS" --argjson att "$ATT" --argjson rs "$RETRY_S" \
+   --argjson iso $ISO --argjson ra "$REASK_S" --argjson dr "$DROPPED" --argjson hk $HANG --argjson ok $OK \
+   --argjson argv "$ARGV_JSON" --arg role "$ROLE" --argjson collab "$COLLAB" \
+   '. + {session_ids:$s, start_ms:$st, end_ms:$en, attempts:$att, retry_s:$rs, retry_isolated:$iso, reask_s:$ra,
+         dropped_lines:$dr, hang_kill:$hk, valid:$ok, role:$role, collab:$collab, argv:$argv}' "$LAST" > "$OUT/$RID.meta.json"
+W_SUM=0; for w in "${WALLS[@]}"; do W_SUM=$(( W_SUM + w )); done; W_SUM=$(( W_SUM + REASK_MS ))
+T_SUM=$REASK_TOK; for t in "${TOKS[@]}"; do T_SUM=$(( T_SUM + t )); done
+jq -n --argjson a "$ATT" --argjson w "$W_SUM" --argjson t "$T_SUM" '{attempts:$a, total_wall_s:($w/1000), total_output_tokens_all:$t}' > "$OUT/$RID.cost.json"
+$OK && exit 0 || exit 1
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py
new file mode 100644
index 000000000..54948b515
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py
@@ -0,0 +1,77 @@
+"""H2 (R-02): truncate over-long anchors and claims in the last findings-v1 block, validate with the real parser.
+
+Usage (from REPO): uv run python tools/h2_normalize.py <in.md> <out.md> <errors.json>
+Writes out.md (only the block lines rewritten) and errors.json = {"ok", "errors": [{"line", "msg"}], "truncated",
+"kept_lines", "dropped_lines"} (kept/dropped = block lines the merge parser keeps / loses).
+Exit 0 always; the caller reads "ok".
+"""
+
+from __future__ import annotations
+
+import json
+import sys
+
+from superclaude.cli.review import findings as fnd
+
+LIMITS = {"anchor": 200, "anchor2": 200, "claim": 300}
+
+
+def normalize(text: str) -> tuple[str, int]:
+    _found, blocks = fnd._blocks_after(text, fnd._HEAD_FINDINGS, "findings-v1")
+    if not blocks:
+        return text, 0
+    lines = text.split("\n")
+    truncated = 0
+    for lineno, raw in blocks[-1][1]:
+        try:
+            obj = json.loads(raw)
+        except json.JSONDecodeError:
+            continue
+        if not isinstance(obj, dict):
+            continue
+        changed = False
+        for key, lim in LIMITS.items():
+            v = obj.get(key)
+            if isinstance(v, str) and len(fnd.flat(v)) > lim:
+                obj[key] = fnd.flat(v)[:lim].rstrip()
+                changed = True
+                truncated += 1
+        if changed:
+            lines[lineno - 1] = json.dumps(obj, ensure_ascii=False)
+    return "\n".join(lines), truncated
+
+
+def dropped_lines(text: str, parsed: dict) -> int:
+    """Block lines the merge parser will not keep (not the number of parser errors).
+
+    With the heading and a block: the non-blank lines of the last block that carry an error. Without the heading,
+    or with no block after it, the parser keeps nothing, so every non-blank line of the last findings-v1 fence in the
+    report is dropped. Block-level notices (several blocks, unclosed block) drop no line by themselves.
+    """
+    found, blocks = fnd._blocks_after(text, fnd._HEAD_FINDINGS, "findings-v1")
+    if found and blocks:
+        body = {ln for ln, raw in blocks[-1][1] if raw.strip()}
+        return len({e["line"] for e in parsed["errors"] if e["line"] in body})
+    _, anywhere = fnd._blocks_after("## Findings block\n" + text, fnd._HEAD_FINDINGS, "findings-v1")
+    return sum(1 for _, raw in anywhere[-1][1] if raw.strip()) if anywhere else 0
+
+
+def main(argv: list[str]) -> int:
+    src, out, errs = argv
+    try:
+        text = open(src, encoding="utf-8").read()
+    except OSError as exc:
+        json.dump({"ok": False, "errors": [{"line": 0, "msg": f"cannot read report: {exc}"}], "truncated": 0,
+                   "kept_lines": 0, "dropped_lines": 0}, open(errs, "w"))
+        open(out, "w").close()
+        return 0
+    new, n = normalize(text)
+    open(out, "w", encoding="utf-8").write(new)
+    parsed = fnd.parse_block(new)
+    json.dump({"ok": parsed["ok"], "errors": parsed["errors"], "truncated": n, "kept_lines": len(parsed["findings"]) + len(parsed["priors"]),
+               "dropped_lines": dropped_lines(new, parsed)}, open(errs, "w"))
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main(sys.argv[1:]))
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/values.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/values.py
new file mode 100644
index 000000000..90622d590
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/values.py
@@ -0,0 +1,222 @@
+# ruff: noqa: N803, N806  (B and G are the design's own symbols)
+"""Timing values (R-41, R-42, R-43, R-45) and the Spike 4 aggregation. DESIGN.md section 2.6.
+
+Usage (from REPO, uv run python tools/values.py ...):
+  spike4 <panel> <row> <row> <row> [...] [--root R1]   write values/<panel>/<pkg>.json (+ .sha256) for the 3 packages
+  show <panel> <pkg> [--root R1]                        print the values file, or the planning fallback
+  deadlines <panel> <pkg> <collab 0|1> <T0_MS> [--root R1]
+      print {"values","FINISH_MS","GUARD_MS","HANG_MS","k","T_report","finish_offset_s","guard_offset_s",
+             "hang_offset_s","B"}; exit 2 when collab 1 has no values file (k cannot be computed)
+All times are seconds from T0. p90 is the nearest-rank 90th percentile.
+"""
+
+from __future__ import annotations
+
+import datetime as dt
+import hashlib
+import json
+import math
+import os
+import statistics
+import sys
+
+R1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
+PKGS = ["TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"]
+G_EL2 = 47.0
+
+
+def _floor(x: float) -> int:
+    return math.floor(round(x, 9))  # 0.35 * 238 - ... must not land on 0.9999999
+
+
+def k_for(B: float, turn: float, trep: float) -> int:
+    """R-42: k = max(0, min(2, floor((0.35 B - 2 - turn - T_report) / (2 turn))))."""
+    return max(0, min(2, _floor((0.35 * B - 2 - turn - trep) / (2 * turn))))
+
+
+def finish_offset(B: float, turn: float, trep: float) -> float:
+    """PANEL_FINISH_AT - T0 = 1.35 B - turn_p90[crit] - T_report_p90[crit]."""
+    return 1.35 * B - turn - trep
+
+
+def guard_g(panel: str, turn_crit: float) -> float:
+    """G = 47 s on el2; Adaptation A-3: 47 x turn_p90[crit] / 6.4 on sl2 and hl2."""
+    return G_EL2 if panel == "el2" else G_EL2 * turn_crit / 6.4
+
+
+def guard_offset(B: float, finish_off: float, G: float) -> float:
+    return min(1.35 * B - G, finish_off)
+
+
+def reader_k_a2(finish_off: float, e_reader: float, turn_reader: float) -> int:
+    """Adaptation A-2 (sl2, hl2 only): the off-path luna role gets its own k from its p90 end time."""
+    return max(0, min(2, _floor((finish_off - e_reader - 2) / (2 * turn_reader))))
+
+
+def compute(panel: str, cfg: dict, B: float, turn: dict, trep: dict, e: dict) -> dict:
+    crit = cfg["critical_role"]
+    fin = finish_offset(B, turn[crit], trep[crit])
+    k = {crit: k_for(B, turn[crit], trep[crit])}
+    other = "searcher" if crit == "reader" else "reader"
+    if panel == "el2":
+        k[other] = k[crit]  # R-42 verbatim on el2
+    else:
+        k[other] = reader_k_a2(fin, e["reader"], turn["reader"])
+    return {"critical_role": crit, "finish_offset_s": fin, "guard_offset_s": guard_offset(B, fin, guard_g(panel, turn[crit])),
+            "hang_offset_s": 1.5 * B, "k": k}
+
+
+def planning(panel: str, cfg: dict) -> dict:
+    crit = cfg["critical_role"]
+    turn = {r: cfg["roles"][r]["planning_turn"] for r in ("searcher", "reader")}
+    trep = dict(turn)
+    trep[crit] = cfg["planning_T_report"]
+    e = {"reader": cfg["planning_reader_end"], "searcher": None}
+    v = compute(panel, cfg, cfg["planning_B"], turn, trep, e)
+    v.update({"panel": panel, "B_f": cfg["planning_B"], "turn_p90": turn, "T_report_p90": trep, "E_p90": e, "values": "planning"})
+    return v
+
+
+def p90(xs: list[float]) -> float:
+    s = sorted(xs)
+    return s[max(0, math.ceil(0.9 * len(s)) - 1)]
+
+
+def _sec(ts: str) -> float:
+    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
+
+
+def turns_of(entries: list) -> tuple[list[float], float | None]:
+    """(inner turn durations, final response duration) of one --output-format json transcript.
+
+    Top-level entries only. A response is the group of assistant entries sharing message.id; its duration is its last
+    timestamp minus the latest tool-result timestamp before it. The first response (no earlier tool result) is left
+    out; the final response feeds only T_report.
+    """
+    groups: list[tuple[float | None, float]] = []
+    last_tr: float | None = None
+    cur_id = None
+    for en in entries:
+        if not isinstance(en, dict) or en.get("parent_tool_use_id") or not en.get("timestamp"):
+            continue
+        ts = _sec(en["timestamp"])
+        msg = en.get("message") or {}
+        if en.get("type") == "assistant":
+            mid = msg.get("id")
+            if groups and mid == cur_id:
+                groups[-1] = (groups[-1][0], max(groups[-1][1], ts))
+            else:
+                groups.append((last_tr, ts))
+                cur_id = mid
+        elif en.get("type") == "user" and any(isinstance(c, dict) and c.get("type") == "tool_result" for c in msg.get("content") or []):
+            last_tr = ts if last_tr is None else max(last_tr, ts)
+            cur_id = None
+    durs = [(end - start) if start is not None else None for start, end in groups]
+    if not durs:
+        return [], None
+    final = durs[-1]
+    inner = [d for d in durs[:-1] if d is not None]
+    return inner, final
+
+
+def _root(argv: list[str]) -> tuple[list[str], str]:
+    if "--root" in argv:
+        i = argv.index("--root")
+        return argv[:i] + argv[i + 2 :], argv[i + 1]
+    return argv, R1
+
+
+def spike4(panel: str, rows: list[str], root: str) -> int:
+    if len(rows) < 3:
+        print(f"REFUSE spike4 needs at least 3 collab-0 rows, got {len(rows)}", file=sys.stderr)
+        return 2
+    cfg = json.load(open(f"{root}/config/panels.json"))[panel]
+    roles = {cfg["roles"]["searcher"]["rid"]: "searcher", **{r: "reader" for r in cfg["roles"]["reader"]["rids"]}}
+    outs = [f"{root}/values/{panel}/{p}.json" for p in PKGS]
+    if any(os.path.exists(o) for o in outs):
+        print("REFUSE values file exists; values are written once", file=sys.stderr)
+        return 2
+    for p, out in zip(PKGS, outs):
+        elapsed, turns, rep, ends = [], {"searcher": [], "reader": []}, {"searcher": [], "reader": []}, {"searcher": [], "reader": []}
+        for row in rows:
+            d = f"{root}/runs/{row}/{p}"
+            t0 = json.load(open(f"{d}/run.json"))["T0_MS"]
+            end_all = []
+            for rid, role in roles.items():
+                meta = json.load(open(f"{d}/reviews/{rid}.meta.json"))
+                end_all.append(meta["end_ms"])
+                ends[role].append((meta["end_ms"] - t0) / 1000)
+                att = f"{d}/reviews/{rid}.attempt{meta['attempts']}.json"
+                try:
+                    entries = json.load(open(att))
+                except (OSError, ValueError):
+                    continue
+                inner, final = turns_of(entries if isinstance(entries, list) else [])
+                turns[role] += inner
+                if final is not None:
+                    rep[role].append(final)
+            elapsed.append((max(end_all) - t0) / 1000)
+        B = statistics.median(elapsed)
+        tp = {r: p90(turns[r]) for r in turns}
+        trp = {r: p90(rep[r]) for r in rep}
+        ep = {r: p90(ends[r]) for r in ends}
+        v = compute(panel, cfg, B, tp, trp, ep)
+        v.update({"panel": panel, "pkg": p, "B_f": B, "turn_p90": tp, "T_report_p90": trp, "E_p90": ep,
+                  "source_runs": rows, "computed_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
+        os.makedirs(os.path.dirname(out), exist_ok=True)
+        body = json.dumps(v, indent=1) + "\n"
+        with open(out, "x") as f:
+            f.write(body)
+        with open(out + ".sha256", "x") as f:
+            f.write(f"{hashlib.sha256(body.encode()).hexdigest()}  {os.path.basename(out)}\n")
+        print(out)
+    return 0
+
+
+def load(panel: str, pkg: str, root: str) -> dict | None:
+    """The values file when it exists and matches its .sha256, else None."""
+    out = f"{root}/values/{panel}/{pkg}.json"
+    if not os.path.exists(out):
+        return None
+    body = open(out, "rb").read()
+    want = open(out + ".sha256").read().split()[0] if os.path.exists(out + ".sha256") else ""
+    if hashlib.sha256(body).hexdigest() != want:
+        raise SystemExit(f"values file {out} does not match its .sha256")
+    v = json.loads(body)
+    v["values"] = want
+    return v
+
+
+def deadlines(panel: str, pkg: str, collab: int, t0: int, root: str) -> int:
+    cfg = json.load(open(f"{root}/config/panels.json"))[panel]
+    v = load(panel, pkg, root)
+    if v is None:
+        if collab == 1:
+            print(f"REFUSE PANEL_COLLAB=1 needs values/{panel}/{pkg}.json (Spike 4)", file=sys.stderr)
+            return 2
+        v = planning(panel, cfg)
+        v["hang_offset_s"] = 2.0 * cfg["planning_B"]  # Spike 4 rows: wider guard so slow rows are not truncated
+    out = {"values": v["values"], "B": v["B_f"], "k": v["k"], "T_report": v["T_report_p90"],
+           "finish_offset_s": v["finish_offset_s"], "guard_offset_s": v["guard_offset_s"], "hang_offset_s": v["hang_offset_s"],
+           "FINISH_MS": t0 + round(1000 * v["finish_offset_s"]), "GUARD_MS": t0 + round(1000 * v["guard_offset_s"]),
+           "HANG_MS": t0 + round(1000 * v["hang_offset_s"])}
+    print(json.dumps(out))
+    return 0
+
+
+def main(argv: list[str]) -> int:
+    argv, root = _root(argv)
+    if argv[:1] == ["spike4"] and len(argv) >= 2:
+        return spike4(argv[1], argv[2:], root)
+    if argv[:1] == ["show"] and len(argv) == 3:
+        v = load(argv[1], argv[2], root) or planning(argv[1], json.load(open(f"{root}/config/panels.json"))[argv[1]])
+        print(json.dumps(v, indent=1))
+        return 0
+    if argv[:1] == ["deadlines"] and len(argv) == 5:
+        return deadlines(argv[1], argv[2], int(argv[3]), int(argv[4]), root)
+    print(__doc__, file=sys.stderr)
+    return 2
+
+
+if __name__ == "__main__":
+    sys.exit(main(sys.argv[1:]))
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/bin/claude b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/bin/claude
new file mode 100755
index 000000000..a0bbf095d
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/bin/claude
@@ -0,0 +1,33 @@
+#!/usr/bin/env bash
+# Test stub for `claude` (never the gateway). Call k follows line k of $STUB_DIR/plan (the last line repeats):
+#   replay <file>        print <file> with @@MODEL@@ replaced by the --model argument
+#   misroute <file>      print <file> with @@MODEL@@ replaced by "gpt-6.1-sol" (a different model)
+#   sleep <s>            sleep, then print nothing
+#   exit <code>          exit with <code> (127 = binary missing)
+#   hooks <n> <file>     run the --settings PostToolUse command n times (exit status ignored, as Claude does), then replay
+# argv is saved to $STUB_DIR/argv.<k> (one token per line) and stdin to $STUB_DIR/stdin.<k>.
+D=${STUB_DIR:?STUB_DIR not set}
+k=$(( $(cat "$D/count" 2>/dev/null || echo 0) + 1 )); echo "$k" > "$D/count"
+printf '%s\n' "$@" > "$D/argv.$k"; cat > "$D/stdin.$k"
+ARGS=("$@"); MODEL=""; SETTINGS=""
+for ((i = 0; i < ${#ARGS[@]}; i++)); do
+  case ${ARGS[i]} in --model) MODEL=${ARGS[i+1]};; --settings) SETTINGS=${ARGS[i+1]};; esac
+done
+line=$(sed -n "${k}p" "$D/plan"); [ -n "$line" ] || line=$(tail -n 1 "$D/plan")
+read -r mode a b <<< "$line"
+replay() { sed "s/@@MODEL@@/$2/g" "$1"; }
+case $mode in
+  replay) replay "$a" "$MODEL";;
+  misroute) replay "$a" "gpt-6.1-sol";;
+  sleep) sleep "$a";;
+  exit) exit "$a";;
+  hooks)
+    cmd=$(printf '%s' "$SETTINGS" | jq -r '.hooks.PostToolUse[0].hooks[0].command')
+    printf '{"type":"user"}\n' > "$D/transcript.jsonl"
+    for ((j = 1; j <= a; j++)); do
+      printf '{"session_id":"stub","transcript_path":"%s","hook_event_name":"PostToolUse","tool_name":"Bash","tool_input":{"command":"ls %s"},"tool_response":{}}' \
+        "$D/transcript.jsonl" "$j" | bash -c "$cmd" >> "$D/hook-out.$k" 2>/dev/null
+      echo "rc=$?" >> "$D/hook-rc.$k"
+    done
+    replay "$b" "$MODEL";;
+esac
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
deleted file mode 100644
index 45ddedcd9..000000000
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
+++ /dev/null
@@ -1,150 +0,0 @@
-"""Shared fixtures for the r1-move-radar tests. Every test writes only under tmp_path."""
-
-from __future__ import annotations
-
-import json
-import os
-import shutil
-import subprocess
-from pathlib import Path
-
-import pytest
-
-R1 = Path(__file__).resolve().parents[1]
-REPO = R1.parents[3]
-A1DIR = REPO / ".dev/eval-workspaces/tasklist-review-panel/20261111-a1"
-FIX = R1 / "tests" / "fixtures"
-TOOLS = R1 / "tools"
-PKG = "TASK-WF-fixture-20261113-000000"
-
-
-def run(args, *, stdin=None, env=None, cwd=None, timeout=60):
-    return subprocess.run(args, input=stdin, capture_output=True, text=True, env=env, cwd=cwd or REPO, timeout=timeout)
-
-
-@pytest.fixture
-def fake_sb(tmp_path):
-    """A sandbox root with one fixture package: SB/<PKG>/repo (root files, src, tests, docs) and SB/cand/<PKG>/."""
-    sb = tmp_path / "sb"
-    repo = sb / PKG / "repo"
-    for rel in ("src/app/core.py", "src/app/scripts/old.sh", "scripts/run.sh", "tests/app/test_core.py",
-                "tests/app/test_other.py", "docs/guide.md", "CHANGELOG.md", "Makefile"):
-        p = repo / rel
-        p.parent.mkdir(parents=True, exist_ok=True)
-        p.write_text("x\n")
-    (repo / "src/app/sub").mkdir()
-    cand = sb / "cand" / PKG
-    cand.mkdir(parents=True)
-    shutil.copy(FIX / "cand" / "candidate.md", cand / "candidate.md")
-    (cand / "source.md").write_text("# source\n")
-    return sb
-
-
-@pytest.fixture
-def root(tmp_path):
-    """A writable R1 output root (index/, runs/, values/ ...) with the real config copied in."""
-    r = tmp_path / "r1"
-    (r / "config").mkdir(parents=True)
-    for f in (R1 / "config").iterdir():
-        shutil.copy(f, r / "config" / f.name)
-    shutil.copy(R1 / "manifest.json", r / "manifest.json")
-    return r
-
-
-def jload(p):
-    return json.loads(Path(p).read_text())
-
-
-@pytest.fixture
-def clean_env():
-    return {k: v for k, v in os.environ.items()}
-
-
-# ---------------------------------------------------------------- hook kit
-SEARCHER, READERS = "t2b-1", ["t4-1", "t3-1"]
-CAT = jload(R1 / "config" / "catalogue.json")
-ORDERS = {"t2b-1": "M2,M7,M4,M1", "t4-1": "M3,M5,M6,M9,M8,M10", "t3-1": "M8,M10,M3,M5,M6,M9",
-          "t1b-1": "M7,M4,M1,M2", "t2-1": "M1,M2,M7,M4"}
-
-
-class Board:
-    """A board under tmp_path with ctx/ files, a clock file and a transcript, driven call by call."""
-
-    def __init__(self, tmp_path, sb="/tmp/sbX"):
-        self.dir = tmp_path / "board"
-        (self.dir / "ctx").mkdir(parents=True)
-        shutil.copy(R1 / "config" / "catalogue.json", self.dir / "ctx" / "catalogue.json")
-        shutil.copy(FIX / "index.json", self.dir / "ctx" / "index.json")
-        self.repo = f"{sb}/{PKG}/repo"
-        self.src = f"{sb}/cand/{PKG}/source.md"
-        (self.dir / "ctx" / "panel.json").write_text(json.dumps({"searcher": SEARCHER, "readers": READERS, "srcpath": self.src}))
-        self.clock = tmp_path / "clock"
-        self.set_clock(1000)
-        self.transcript = tmp_path / "transcript.jsonl"
-        self.transcript.write_text('{"type":"user"}\n{"type":"assistant"}\n')
-
-    def set_clock(self, ms):
-        self.clock.write_text(str(ms))
-
-    def stdin(self, tool="Bash", inp=None, agent_id=None, transcript=None):
-        d = {"session_id": "s1", "transcript_path": str(transcript or self.transcript), "hook_event_name": "PostToolUse",
-             "tool_name": tool, "tool_input": inp if inp is not None else {"command": "ls"}, "tool_response": {}}
-        if agent_id:
-            d["agent_id"] = agent_id
-        return json.dumps(d)
-
-    def args(self, rid, role, k=2, cps=None, finish=10**9, guard=10**9, order=None):
-        cps = cps or ((6, 10) if role == "searcher" else (8, 12))
-        return [str(self.dir), "row-c1-r0/" + PKG, rid, role, "0", str(finish), str(guard), str(k), str(cps[0]),
-                str(cps[1]), order or ORDERS[rid], PKG, str(self.clock)]
-
-    def call(self, rid, role, env=None, raw_stdin=None, **kw):
-        a = self.args(rid, role, **{k: v for k, v in kw.items() if k in ("k", "cps", "finish", "guard", "order")})
-        s = raw_stdin if raw_stdin is not None else self.stdin(**{k: v for k, v in kw.items() if k in ("tool", "inp", "agent_id", "transcript")})
-        r = run(["bash", str(TOOLS / "radar-hook.sh"), *a], stdin=s, env=env)
-        assert r.returncode == 0, r.stderr
-        return r.stdout.strip()
-
-    def metrics(self, rid):
-        p = self.dir / "metrics" / f"{rid}.jsonl"
-        return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
-
-    def metrics_safe(self, rid):
-        """Metrics lines that are JSON objects (a test may plant junk lines)."""
-        p = self.dir / "metrics" / f"{rid}.jsonl"
-        out = []
-        for x in p.read_text().splitlines() if p.exists() else []:
-            try:
-                v = json.loads(x)
-            except ValueError:
-                continue
-            if isinstance(v, dict):
-                out.append(v)
-        return out
-
-    def events(self, rid, ev):
-        return [m for m in self.metrics(rid) if m.get("ev") == ev]
-
-    def tele(self, rid, line):
-        p = self.dir / "tele" / f"{rid}.jsonl"
-        p.parent.mkdir(exist_ok=True)
-        with p.open("a") as f:
-            f.write(line + "\n")
-
-
-def expected_text(move, role):
-    if move is None:
-        return CAT["src_text"]
-    return CAT["moves"][move] + (CAT["observable_suffix"] if role == "searcher" and move in CAT["observable"] else "")
-
-
-def ctx_text(out):
-    d = json.loads(out)
-    assert list(d) == ["hookSpecificOutput"] and d["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
-    assert set(d["hookSpecificOutput"]) == {"hookEventName", "additionalContext"}
-    return d["hookSpecificOutput"]["additionalContext"]
-
-
-@pytest.fixture
-def board(tmp_path):
-    return Board(tmp_path)
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
index 000000000..397445d8b 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
@@ -11,7 +11,7 @@ from pathlib import Path
 import pytest
 
 R1 = Path(__file__).resolve().parents[1]
-REPO = R1.parents[3]
+REPO = R1.parents[4]
 A1DIR = REPO / ".dev/eval-workspaces/tasklist-review-panel/20261111-a1"
 FIX = R1 / "tests" / "fixtures"
 TOOLS = R1 / "tools"
@@ -148,3 +148,98 @@ def ctx_text(out):
 @pytest.fixture
 def board(tmp_path):
     return Board(tmp_path)
+
+
+# ---------------------------------------------------------------- runner kit (stub claude, never the gateway)
+STUB_BIN = FIX / "bin"
+ANCHOR = "Create `src/app/merge_guard.py` and `src/app/scripts/tool.sh`"
+
+
+def finding(**kw):
+    f = {"id": "F1", "severity": "MAJOR", "blocking": True, "category": "contradiction", "anchor": ANCHOR,
+         "refs": [], "claim": "The module and the script disagree."}
+    f.update(kw)
+    return f
+
+
+def report(*findings_, raw_lines=()):
+    body = "\n".join([json.dumps(f) for f in findings_] + list(raw_lines))
+    return f"review: 1 of 3\n\nCovered everything.\n\n## Findings block\n\n```findings-v1\n{body}\n```\n\nverdict: FAIL\n"
+
+
+def json_reply(text, session="sess-1", tokens=100, model="@@MODEL@@"):
+    return json.dumps([
+        {"type": "system", "subtype": "init"},
+        {"type": "assistant", "timestamp": "2026-11-13T10:00:01.000Z", "parent_tool_use_id": None,
+         "message": {"id": "m1", "model": model, "content": [{"type": "text", "text": "ok"}]}},
+        {"type": "result", "subtype": "success", "result": text, "session_id": session,
+         "usage": {"output_tokens": tokens}, "modelUsage": {model: {"outputTokens": tokens}}}])
+
+
+def stream_reply(text, session="sess-1", tokens=50):
+    return "\n".join(json.dumps(x) for x in [
+        {"type": "system", "subtype": "init", "session_id": session},
+        {"type": "assistant", "message": {"id": "m2", "model": "@@MODEL@@", "content": [{"type": "text", "text": text}]}},
+        {"type": "result", "subtype": "success", "result": text, "session_id": session,
+         "modelUsage": {"@@MODEL@@": {"outputTokens": tokens}}}]) + "\n"
+
+
+class Runner:
+    """runs/<row>/<pkg>/ with run.json under a tmp R1 root, a tmp sandbox and a stub plan."""
+
+    def __init__(self, tmp_path, root, hang_s=600, row="el2-c1-r0"):
+        self.root, self.row = root, row
+        self.sb = tmp_path / "sb"
+        (self.sb / PKG / "repo").mkdir(parents=True)
+        (self.sb / "cand" / PKG).mkdir(parents=True)
+        shutil.copy(FIX / "cand" / "candidate.md", self.sb / "cand" / PKG / "candidate.md")
+        (self.sb / "cand" / PKG / "source.md").write_text("# source\n")
+        self.d = root / "runs" / row / PKG
+        (self.d / "settings").mkdir(parents=True)
+        import time
+        t0 = int(time.time() * 1000)
+        self.t0 = t0
+        self.write_run(hang_ms=t0 + int(hang_s * 1000))
+        self.stub = tmp_path / "stub"
+        self.stub.mkdir()
+        self.n = 0
+        self.env = dict(os.environ, PATH=f"{STUB_BIN}:{os.environ['PATH']}", NOFALLBACK="1", STUB_DIR=str(self.stub))
+
+    def write_run(self, hang_ms):
+        (self.d / "run.json").write_text(json.dumps({"T0_MS": self.t0, "HANG_MS": hang_ms, "FINISH_MS": hang_ms, "GUARD_MS": hang_ms,
+                                                     "role": {"t2b-1": "searcher", "t4-1": "reader", "t3-1": "reader"},
+                                                     "T_report": {"searcher": 1, "reader": 1}}))
+
+    def file(self, content):
+        self.n += 1
+        p = self.stub / f"reply{self.n}"
+        p.write_text(content)
+        return p
+
+    def plan(self, *lines):
+        (self.stub / "plan").write_text("\n".join(lines) + "\n")
+
+    def settings(self, rid, board="/nonexistent/board"):
+        r = run(["bash", str(TOOLS / "settings-gen.sh"), board, f"{self.row}/{PKG}", rid, "searcher", "0", "99999999999999", "99999999999999", "2", "6",
+                 "10", "M2,M7,M4,M1", PKG, ""])
+        (self.d / "settings" / f"{rid}.json").write_text(r.stdout)
+        return r.stdout.strip()
+
+    def run(self, rid="t2b-1", model="muse-ember-1.0", collab=1, print_cmd=False, timeout=120):
+        a = ["bash", str(TOOLS / "run-reviewer.sh")] + (["--print-cmd"] if print_cmd else []) + \
+            [self.row, PKG, rid, model, str(collab), str(self.t0), "--root", str(self.root), "--sb", str(self.sb)]
+        return run(a, env=self.env, timeout=timeout)
+
+    def meta(self, rid="t2b-1"):
+        return jload(self.d / "reviews" / f"{rid}.meta.json")
+
+    def argv(self, k):
+        return (self.stub / f"argv.{k}").read_text().splitlines()
+
+    def calls(self):
+        return int((self.stub / "count").read_text()) if (self.stub / "count").exists() else 0
+
+
+@pytest.fixture
+def runner(tmp_path, root):
+    return Runner(tmp_path, root)
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/cand/candidate.md b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/cand/candidate.md
deleted file mode 100644
index fae29b27f..000000000
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/cand/candidate.md
+++ /dev/null
@@ -1,27 +0,0 @@
----
-schema: workflow-plan/1.2
----
-
-# Fixture plan
-
-## Constraints
-
-- Keep `src/app/core.py` importable.
-
-## Task 1: Add the guard module
-
-Create `src/app/merge_guard.py` and `src/app/scripts/tool.sh`, and extend `src/app/core.py`.
-
-Acceptance criteria:
-- `grep -n "merge_guard" src/app/core.py` prints one line.
-
-## Task 2: Update the docs
-
-Edit `docs/guide.md` and `CHANGELOG.md`; model the helper on `scripts/old.sh` and call `scripts/tool.sh`.
-
-Acceptance criteria:
-- `grep -rl HOW-WE-WORK tests` prints nothing.
-
-## Task 3: Tests
-
-Add `tests/app/test_merge_guard.py`; keep `tests/app/test_core.py` green.
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/cand/candidate.md
index 000000000..792c17e7a 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/cand/candidate.md
@@ -25,3 +25,5 @@ Acceptance criteria:
 ## Task 3: Tests
 
 Add `tests/app/test_merge_guard.py`; keep `tests/app/test_core.py` green.
+
+The guard keeps every retry visible to the operator, records each attempt with its reason and its outcome, refuses to hide a failed attempt behind a later success, and reports the full history of the cycle when the run ends so that nobody has to reconstruct it from scattered logs or from memory afterwards
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_h2.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_h2.py
new file mode 100644
index 000000000..a1161b3d9
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_h2.py
@@ -0,0 +1,112 @@
+"""T-11: H2 normaliser and the one re-ask (R-02)."""
+
+import json
+
+from conftest import (
+    FIX,
+    REPO,
+    TOOLS,
+    finding,
+    jload,
+    json_reply,
+    report,
+    run,
+    stream_reply,
+)
+
+from superclaude.cli.review import findings as fnd
+
+CAND = (FIX / "cand" / "candidate.md").read_text()
+LONG = CAND[CAND.index("The guard keeps"):].strip()
+
+
+def h2(tmp_path, text):
+    src, out, errs = tmp_path / "in.md", tmp_path / "out.md", tmp_path / "h2.json"
+    src.write_text(text)
+    r = run(["uv", "run", "python", str(TOOLS / "h2_normalize.py"), str(src), str(out), str(errs)], cwd=REPO)
+    assert r.returncode == 0, r.stderr
+    return out.read_text(), jload(errs)
+
+
+def test_long_anchor_truncated_and_still_located(tmp_path):
+    anchor = LONG[:250]
+    assert len(anchor) == 250
+    out, e = h2(tmp_path, report(finding(anchor=anchor)))
+    f = fnd.parse_block(out)["findings"][0]
+    assert len(f["anchor"]) <= 200 and anchor.startswith(f["anchor"]) and e["ok"] and e["truncated"] == 1
+    assert fnd.locate(CAND, f["anchor"])
+
+
+def test_long_claim_truncated(tmp_path):
+    out, e = h2(tmp_path, report(finding(claim="x" * 400)))
+    assert len(fnd.parse_block(out)["findings"][0]["claim"]) == 300 and e["ok"]
+
+
+def test_bad_severity_reported(tmp_path):
+    _, e = h2(tmp_path, report(finding(), finding(id="F2", severity="HIGH")))
+    assert not e["ok"] and any("severity" in x["msg"] for x in e["errors"])
+
+
+def test_only_block_lines_rewritten(tmp_path):
+    text = report(finding(claim="y" * 400))
+    out, _ = h2(tmp_path, text)
+    a, b = text.splitlines(), out.splitlines()
+    assert len(a) == len(b) and [i for i, (x, y) in enumerate(zip(a, b)) if x != y] == [a.index(json.dumps(finding(claim="y" * 400)))]
+
+
+def _bad():
+    return report(finding(), finding(id="F2", severity="HIGH"))
+
+
+def test_reask_still_bad_drops_line(runner):
+    runner.plan(f"replay {runner.file(json_reply(_bad()))}", f"replay {runner.file(stream_reply(_bad()))}")
+    r = runner.run(collab=0)
+    assert r.returncode == 0, r.stderr
+    m = runner.meta()
+    assert m["dropped_lines"] == 1 and isinstance(m["reask_s"], (int, float)) and runner.calls() == 2
+    a2 = runner.argv(2)
+    assert "--resume" in a2 and a2[a2.index("--resume") + 1] == "sess-1" and "stream-json" in a2 and "--settings" not in a2
+    assert "parser errors" in (runner.stub / "stdin.2").read_text()
+
+
+def test_reask_good_gives_zero_dropped(runner):
+    runner.plan(f"replay {runner.file(json_reply(_bad()))}", f"replay {runner.file(stream_reply(report(finding())))}")
+    assert runner.run(collab=0).returncode == 0
+    m = runner.meta()
+    assert m["dropped_lines"] == 0 and m["reask_s"] is not None
+    assert fnd.parse_block((runner.d / "reviews" / "t2b-1.md").read_text())["ok"]
+    assert jload(runner.d / "reviews" / "t2b-1.cost.json")["total_output_tokens_all"] == 150  # attempt 100 + re-ask 50
+
+
+def test_no_reask_when_clean(runner):
+    runner.plan(f"replay {runner.file(json_reply(report(finding())))}")
+    assert runner.run(collab=0).returncode == 0
+    assert runner.calls() == 1 and runner.meta()["reask_s"] is None and runner.meta()["dropped_lines"] == 0
+
+
+def test_dropped_counts_lines_not_errors(tmp_path):
+    # one bad line among two: 1 dropped, 1 kept
+    _, e = h2(tmp_path, report(finding(), finding(id="F2", severity="HIGH")))
+    assert e["dropped_lines"] == 1 and e["kept_lines"] == 1
+    # wrong heading: the parser keeps nothing, both block lines are dropped (one line-0 error only)
+    text = report(finding(), finding(id="F2")).replace("## Findings block", "## Findings")
+    _, e = h2(tmp_path, text)
+    assert len(e["errors"]) == 1 and e["dropped_lines"] == 2 and e["kept_lines"] == 0
+    # two blocks: a block-level notice, no dropped line
+    two = report(finding()) + "\n```findings-v1\n" + json.dumps(finding(id="F9")) + "\n```\n"
+    _, e = h2(tmp_path, two)
+    assert not e["ok"] and e["dropped_lines"] == 0 and e["kept_lines"] == 1
+
+
+def test_runner_wrong_heading_reports_all_lines_dropped(runner):
+    text = report(finding(), finding(id="F2")).replace("## Findings block", "## Findings")
+    runner.plan(f"replay {runner.file(json_reply(text))}", f"replay {runner.file(stream_reply(text))}")
+    assert runner.run(collab=0).returncode == 0
+    assert runner.meta()["dropped_lines"] == 2 and runner.calls() == 2
+
+
+def test_reask_with_fewer_kept_lines_is_not_taken(runner):
+    runner.plan(f"replay {runner.file(json_reply(_bad()))}", f"replay {runner.file(stream_reply(report()))}")
+    assert runner.run(collab=0).returncode == 0
+    m = runner.meta()
+    assert m["dropped_lines"] == 1 and len(fnd.parse_block((runner.d / "reviews" / "t2b-1.md").read_text())["findings"]) == 1
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_values.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_values.py
new file mode 100644
index 000000000..757f6150c
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_values.py
@@ -0,0 +1,99 @@
+# ruff: noqa: N803  (B is the design's own symbol)
+"""T-12: timing values and the Spike 4 turn extraction (R-41..R-43)."""
+
+import importlib.util
+import json
+
+import pytest
+from conftest import TOOLS, jload, run
+
+spec = importlib.util.spec_from_file_location("values", TOOLS / "values.py")
+V = importlib.util.module_from_spec(spec)
+spec.loader.exec_module(V)
+
+
+def ts(s):
+    return f"2026-11-13T10:00:{s:06.3f}Z"
+
+
+def attempt_fixture():
+    a = lambda mid, t, kind="text": {"type": "assistant", "timestamp": ts(t), "parent_tool_use_id": None,  # noqa: E731
+                                     "message": {"id": mid, "content": [{"type": kind}]}}
+    tr = lambda t: {"type": "user", "timestamp": ts(t), "parent_tool_use_id": None,  # noqa: E731
+                    "message": {"content": [{"type": "tool_result"}]}}
+    return [
+        {"type": "system", "subtype": "init"},                      # untimed
+        a("r1", 1.0, "thinking"), a("r1", 1.5, "tool_use"),          # first response: no earlier tool result -> no turn
+        tr(2.0),
+        a("r2", 3.0, "thinking"), a("r2", 3.5, "tool_use"), a("r2", 4.0, "tool_use"),  # split over 3 entries, 2 parallel calls
+        tr(4.5), tr(4.6),
+        a("r3", 6.6, "tool_use"),                                    # 2.0 s after the latest tool result
+        tr(7.0),
+        {"type": "assistant", "timestamp": ts(8.0), "parent_tool_use_id": "sub", "message": {"id": "s1"}},  # subagent: ignored
+        a("r4", 9.0, "thinking"), a("r4", 27.0, "text"),             # final report response: 20 s
+        {"type": "result", "result": "x"},
+    ]
+
+
+def test_turn_extraction():
+    inner, final = V.turns_of(attempt_fixture())
+    assert inner == pytest.approx([2.0, 2.0])  # r2: 4.0 - 2.0; r3: 6.6 - 4.6; r1 left out
+    assert final == pytest.approx(20.0)
+
+
+@pytest.mark.parametrize("B,turn,trep,k", [(116, 6.4, 6.4, 2), (116, 6.4, 11.0, 1), (100, 6.4, 13.8, 1), (100, 6.4, 13.9, 0),
+                                            # SL2: the exact bound is 51.795 s, which the design rounds to 51.8
+                                            (273.7, 14, 51.79, 1), (273.7, 14, 51.81, 0), (238, 23, 23, 0), (238, 23, 12.3, 1),
+                                            (238, 23, 12.4, 0)])
+def test_r42(B, turn, trep, k):
+    assert V.k_for(B, turn, trep) == k
+
+
+def test_planning_values():
+    cfg = jload(TOOLS.parent / "config" / "panels.json")
+    el2, sl2, hl2 = (V.planning(p, cfg[p]) for p in ("el2", "sl2", "hl2"))
+    assert el2["finish_offset_s"] == pytest.approx(143.8, abs=0.1)
+    assert el2["guard_offset_s"] == pytest.approx(109.6, abs=0.1)
+    assert sl2["guard_offset_s"] == pytest.approx(266.7, abs=0.1)
+    assert hl2["guard_offset_s"] == pytest.approx(152.4, abs=0.1)
+    assert hl2["k"] == {"searcher": 0, "reader": 2}  # A-2 reader k on hl2 planning
+    assert el2["k"] == {"reader": 2, "searcher": 2}  # el2 never uses A-2: reader k = searcher k = crit k
+    # el2 with a slow reader: the searcher still takes the critical k (no A-2)
+    v = V.compute("el2", cfg["el2"], 116, {"searcher": 3.2, "reader": 6.4}, {"searcher": 3.2, "reader": 11.0}, {"reader": 140})
+    assert v["k"] == {"reader": 1, "searcher": 1}
+    assert el2["hang_offset_s"] == pytest.approx(174)
+
+
+def _row(root, row, pkg, t0, ends, attempt):
+    d = root / "runs" / row / pkg
+    (d / "reviews").mkdir(parents=True)
+    (d / "run.json").write_text(json.dumps({"T0_MS": t0}))
+    for rid, end in ends.items():
+        (d / "reviews" / f"{rid}.meta.json").write_text(json.dumps({"end_ms": end, "attempts": 1}))
+        (d / "reviews" / f"{rid}.attempt1.json").write_text(json.dumps(attempt))
+
+
+def test_spike4_refusals_and_write(root):
+    pk = V.PKGS
+    for i, row in enumerate(["el2-c0-r1", "el2-c0-r2", "el2-c0-r3"]):
+        for p in pk:
+            _row(root, row, p, 0, {"t2b-1": 100_000 + i * 1000, "t4-1": 110_000, "t3-1": 120_000 + i * 2000}, attempt_fixture())
+    r = run(["uv", "run", "python", str(TOOLS / "values.py"), "spike4", "el2", "el2-c0-r1", "el2-c0-r2", "--root", str(root)])
+    assert r.returncode == 2 and "at least 3" in r.stderr
+    r = run(["uv", "run", "python", str(TOOLS / "values.py"), "spike4", "el2", "el2-c0-r1", "el2-c0-r2", "el2-c0-r3", "--root", str(root)])
+    assert r.returncode == 0, r.stderr
+    v = jload(root / "values" / "el2" / f"{pk[0]}.json")
+    assert v["B_f"] == pytest.approx(122.0) and v["turn_p90"]["reader"] == pytest.approx(2.0) and v["T_report_p90"]["reader"] == pytest.approx(20.0)
+    assert (root / "values" / "el2" / f"{pk[0]}.json.sha256").exists()
+    r = run(["uv", "run", "python", str(TOOLS / "values.py"), "spike4", "el2", "el2-c0-r1", "el2-c0-r2", "el2-c0-r3", "--root", str(root)])
+    assert r.returncode == 2 and "written once" in r.stderr
+    d = json.loads(run(["uv", "run", "python", str(TOOLS / "values.py"), "deadlines", "el2", pk[0], "1", "1000", "--root", str(root)]).stdout)
+    assert d["HANG_MS"] == 1000 + round(1000 * 1.5 * 122.0) and d["values"] != "planning"
+
+
+def test_deadlines_planning_and_refusal(root):
+    pk = V.PKGS[0]
+    r = run(["uv", "run", "python", str(TOOLS / "values.py"), "deadlines", "sl2", pk, "1", "0", "--root", str(root)])
+    assert r.returncode == 2
+    d = json.loads(run(["uv", "run", "python", str(TOOLS / "values.py"), "deadlines", "sl2", pk, "0", "0", "--root", str(root)]).stdout)
+    assert d["values"] == "planning" and d["HANG_MS"] == round(1000 * 2.0 * 273.7)  # 547.4 s
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_runner_retry.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_runner_retry.py
new file mode 100644
index 000000000..be8bd8ae4
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_runner_retry.py
@@ -0,0 +1,36 @@
+"""T-13: retry isolation and no fallback (R-44, NOFALLBACK)."""
+
+from conftest import finding, jload, json_reply, report
+
+
+def test_no_block_then_isolated_retry(runner):
+    runner.settings("t2b-1")
+    runner.plan(f"replay {runner.file(json_reply('no block here'))}", f"replay {runner.file(json_reply(report(finding())))}")
+    r = runner.run(collab=1)
+    assert r.returncode == 0, r.stderr
+    assert "--settings" in runner.argv(1) and "--settings" not in runner.argv(2)
+    m = runner.meta()
+    assert m["retry_isolated"] is True and m["attempts"] == 2 and m["valid"] is True and m["retry_s"] is not None
+    c = jload(runner.d / "reviews" / "t2b-1.cost.json")
+    a1 = jload(runner.d / "reviews" / "t2b-1.attempt1.meta.json")
+    a2 = jload(runner.d / "reviews" / "t2b-1.attempt2.meta.json")
+    assert c["attempts"] == 2 and c["total_wall_s"] == (a1["wall_ms"] + a2["wall_ms"]) / 1000
+    assert c["total_output_tokens_all"] == 200
+
+
+def test_misroute_twice_invalid_no_fallback(runner):
+    f = runner.file(json_reply(report(finding())))
+    runner.plan(f"misroute {f}")
+    r = runner.run(collab=0)
+    assert r.returncode == 1
+    assert runner.calls() == 2  # no third attempt
+    for k in (1, 2):
+        a = runner.argv(k)
+        assert a[a.index("--model") + 1] == "muse-ember-1.0"  # no other model is ever invoked
+    m = runner.meta()
+    assert m["valid"] is False and m["model_ok"] is False and m["observed_model"] == "gpt-6.1-sol"
+
+
+def test_refuses_without_nofallback(runner):
+    runner.env.pop("NOFALLBACK")
+    assert runner.run(collab=0).returncode == 2 and runner.calls() == 0
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_settings_and_cmd.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_settings_and_cmd.py
deleted file mode 100644
index c202237b3..000000000
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_settings_and_cmd.py
+++ /dev/null
@@ -1,27 +0,0 @@
-"""T-10 (settings part): settings-gen.sh output."""
-
-import json
-
-from conftest import TOOLS, run
-
-
-def test_settings_json(tmp_path):
-    board = str(tmp_path / "runs" / "el2-c1-r0" / "P" / "board")
-    args = [board, "el2-c1-r0/P", "t4-1", "reader", "1763062000000", "1763062143800", "1763062109600", "2", "8", "12",
-            "M3,M5,M6,M9,M8,M10", "P", ""]
-    r = run(["bash", str(TOOLS / "settings-gen.sh"), *args])
-    assert r.returncode == 0, r.stderr
-    d = json.loads(r.stdout)
-    h = d["hooks"]["PostToolUse"]
-    assert len(h) == 1 and h[0]["matcher"] == "*" and len(h[0]["hooks"]) == 1
-    cmd = h[0]["hooks"][0]
-    assert cmd["type"] == "command" and cmd["timeout"] == 5
-    assert "$" not in r.stdout
-    for v in (board, "'t4-1'", "'1763062000000'", "'1763062143800'", str(TOOLS / "radar-hook.sh")):
-        assert v in cmd["command"]
-    assert cmd["command"].endswith(" ''")
-
-
-def test_settings_refuses_unsafe_value(tmp_path):
-    args = ["/b", "r", "t4-1", "reader", "0", "1", "1", "2", "8", "12", "M3", "P$(id)", ""]
-    assert run(["bash", str(TOOLS / "settings-gen.sh"), *args]).returncode == 2
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_settings_and_cmd.py
index 000000000..e6c73c5d2 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_settings_and_cmd.py
@@ -25,3 +25,41 @@ def test_settings_json(tmp_path):
 def test_settings_refuses_unsafe_value(tmp_path):
     args = ["/b", "r", "t4-1", "reader", "0", "1", "1", "2", "8", "12", "M3", "P$(id)", ""]
     assert run(["bash", str(TOOLS / "settings-gen.sh"), *args]).returncode == 2
+
+
+# ---------------------------------------------------------------- T-10 (cmd part, R-05)
+def a1_tokens():
+    import shlex
+
+    from conftest import A1DIR
+    line = (A1DIR / "tools" / "run-reviewer.sh").read_text().splitlines()[47]  # line 48
+    inner = line[line.index("&& ") + 3: line.index(" <<<")]
+    return shlex.split(inner)
+
+
+def allowed(tokens, model, hang):
+    """Apply exactly the R-05 allowed set to the A1 token list."""
+    t = [model if x == "$MODEL" else x for x in tokens]
+    i = t.index("timeout")
+    assert t[i + 1] == "3000"
+    t[i:i + 2] = ["timeout", "--kill-after=5", hang]
+    t.remove("--no-session-persistence")
+    return t
+
+
+def test_print_cmd_collab0_matches_a1(runner):
+    import json
+    d = json.loads(runner.run(collab=0, print_cmd=True).stdout)
+    argv = d["argv"]
+    assert argv == allowed(a1_tokens(), "muse-ember-1.0", argv[2]) and argv[2].isdigit()
+    assert "--settings" not in argv and "--no-session-persistence" not in argv
+    assert d["cwd"] == str(runner.sb / runner.d.name / "repo")
+    assert str(runner.sb / "cand" / runner.d.name / "candidate.md") in d["stdin"]
+    assert "The plan's source document is " + str(runner.sb / "cand" / runner.d.name / "source.md") in d["stdin"]
+
+
+def test_print_cmd_collab1_only_adds_settings(runner):
+    import json
+    s = runner.settings("t2b-1")
+    argv = json.loads(runner.run(collab=1, print_cmd=True).stdout)["argv"]
+    assert argv == allowed(a1_tokens(), "muse-ember-1.0", argv[2]) + ["--settings", s]
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py
deleted file mode 100644
index cdac35697..000000000
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py
+++ /dev/null
@@ -1,35 +0,0 @@
-"""Fault-injection tests F-1..F-14 (DESIGN.md section 6.2)."""
-
-import json
-
-from conftest import ctx_text
-
-
-# F-6: snapshot failure -> snapshot_missing 1, zero deliveries (same mechanism as T-7)
-def test_f6_snapshot_failure(board, tmp_path):
-    outs = [board.call("t4-1", "reader", transcript=tmp_path / "nope.jsonl") for _ in range(13)]
-    assert all(o == "" for o in outs)
-    assert len(board.events("t4-1", "snapshot_missing")) == 1 and board.events("t4-1", "inject") == []
-
-
-# F-7: a garbage line in tele/ does not change the hook's output
-def test_f7_corrupt_board_line(board, tmp_path):
-    from conftest import Board
-    clean = Board(tmp_path / "clean")
-    board.tele("t2b-1", "\x00garbage{")
-    a = [board.call("t2b-1", "searcher") for _ in range(10)]
-    b = [clean.call("t2b-1", "searcher") for _ in range(10)]
-    assert [bool(x) for x in a] == [bool(x) for x in b] and ctx_text(a[9]) == ctx_text(b[9])
-
-
-# F-14: env -i PATH=/usr/bin:/bin gives the same decisions and outputs
-def test_f14_environment_cleared(board, tmp_path):
-    from conftest import Board
-    other = Board(tmp_path / "envi")
-    env = {"PATH": "/usr/bin:/bin"}
-    a = [board.call("t2b-1", "searcher") for _ in range(11)]
-    b = [other.call("t2b-1", "searcher", env=env) for _ in range(11)]
-    assert a == b
-    strip = lambda evs: [{k: v for k, v in e.items() if k not in ("ms",)} for e in evs if e["ev"] != "t"]  # noqa: E731
-    assert strip(board.metrics("t2b-1")) == strip(other.metrics("t2b-1"))
-    assert json.loads(a[5]) and json.loads(a[9])
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py
index 000000000..138dab799 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py
@@ -33,3 +33,52 @@ def test_f14_environment_cleared(board, tmp_path):
     strip = lambda evs: [{k: v for k, v in e.items() if k not in ("ms",)} for e in evs if e["ev"] != "t"]  # noqa: E731
     assert strip(board.metrics("t2b-1")) == strip(other.metrics("t2b-1"))
     assert json.loads(a[5]) and json.loads(a[9])
+
+
+# ---------------------------------------------------------------- runner faults (stub claude)
+def test_f8_hang_killed_at_deadline(runner):
+    import time
+    for collab in (1, 0):
+        if collab:
+            runner.settings("t2b-1")
+        runner.write_run(hang_ms=int(time.time() * 1000) + 3000)
+        (runner.stub / "count").unlink(missing_ok=True)
+        runner.plan("sleep 60")
+        t = time.time()
+        r = runner.run(collab=collab)
+        took = time.time() - t
+        assert r.returncode == 1 and took < 3 + 5 + 3  # TERM at the deadline, KILL at most 5 s later (+ start-up)
+        m = runner.meta()
+        assert m["hang_kill"] is True and m["valid"] is False and runner.calls() == 1  # no time left for a retry
+
+
+def test_f9_failed_block_then_isolated_retry(runner):
+    from conftest import finding, json_reply, report
+    runner.settings("t2b-1")
+    runner.plan(f"replay {runner.file(json_reply('incomplete'))}", f"replay {runner.file(json_reply(report(finding())))}")
+    assert runner.run(collab=1).returncode == 0
+    m = runner.meta()
+    assert m["attempts"] == 2 and m["retry_isolated"] is True and "--settings" not in runner.argv(2)
+
+
+def test_f10_binary_missing_twice(runner):
+    runner.plan("exit 127")
+    r = runner.run(collab=0)
+    assert r.returncode == 1 and runner.calls() == 2
+    assert all(runner.argv(k)[runner.argv(k).index("--model") + 1] == "muse-ember-1.0" for k in (1, 2))
+    assert runner.meta()["valid"] is False and not (runner.d / "reviews" / "t2b-1.fallback.log").exists()
+
+
+def test_f13_hook_error_does_not_kill_review(runner, tmp_path):
+    """The stub runs the real hook from --settings for 8 tool calls; the hook's inputs break mid-run."""
+    from conftest import Board, finding, json_reply, report
+    b = Board(tmp_path / "f13")
+    s = runner.settings("t2b-1", board=str(b.dir))
+    assert str(b.dir) in s
+    (b.dir / "ctx" / "index.json").write_text("{broken")  # every checkpoint now fails inside the hook
+    runner.plan(f"hooks 8 {runner.file(json_reply(report(finding())))}")
+    r = runner.run(collab=1)
+    assert r.returncode == 0, r.stderr
+    assert runner.meta()["valid"] is True
+    assert [m for m in b.metrics("t2b-1") if m["ev"] == "hook_error"]
+    assert all(x == "rc=0" for x in (runner.stub / "hook-rc.1").read_text().split())

Codegraph context
index_state=fresh checked_at=2026-11-13T20:27:49Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b: the changed files are shell, jq, JSON and Python under .dev (eval harness, no product symbols have dependents outside the touched set); dependents checked on the Grep/Read floor: none outside the touched set.
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh
index 000000000..7dc3fc7f4 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh
@@ -106,13 +106,15 @@ Reply with the complete corrected report, ending with the ## Findings block and
     [ -n "$rsid" ] && [ "$rsid" != "$SID" ] && { SIDS+=("$rsid"); partial_meta; }
     if [ -s "$OUT/$RID.reask.md" ]; then
       h2 "$OUT/$RID.reask.md" "$OUT/$RID.norm2.md" "$OUT/$RID.h2-reask.json"
-      # the re-ask answer replaces the first report unless it parses worse (more errors) than what we have
-      if [ "$(jq '.errors|length' "$OUT/$RID.h2-reask.json")" -le "$(jq '.errors|length' "$OUT/$RID.h2.json")" ]; then
+      # the re-ask answer replaces the first report unless the merge would keep fewer of its lines
+      # (more kept lines wins; on a tie, fewer dropped lines wins)
+      if jq -e -n --slurpfile a "$OUT/$RID.h2-reask.json" --slurpfile b "$OUT/$RID.h2.json" \
+           '[$a[0].kept_lines, -$a[0].dropped_lines] >= [$b[0].kept_lines, -$b[0].dropped_lines]' >/dev/null; then
         mv "$OUT/$RID.norm2.md" "$OUT/$RID.norm.md"; cp "$OUT/$RID.h2-reask.json" "$OUT/$RID.h2.json"
       fi
     fi
   fi
-  DROPPED=$(jq '.errors|length' "$OUT/$RID.h2.json")
+  DROPPED=$(jq '.dropped_lines' "$OUT/$RID.h2.json")  # block lines the merge parser will not keep
   cp "$OUT/$RID.norm.md" "$OUT/$RID.md"
 else
   cp "$OUT/$RID.attempt$ATT.md" "$OUT/$RID.md" 2>/dev/null || : > "$OUT/$RID.md"
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py
index 000000000..54948b515 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py
@@ -1,7 +1,8 @@
 """H2 (R-02): truncate over-long anchors and claims in the last findings-v1 block, validate with the real parser.
 
 Usage (from REPO): uv run python tools/h2_normalize.py <in.md> <out.md> <errors.json>
-Writes out.md (only the block lines rewritten) and errors.json = {"ok", "errors": [{"line", "msg"}], "truncated"}.
+Writes out.md (only the block lines rewritten) and errors.json = {"ok", "errors": [{"line", "msg"}], "truncated",
+"kept_lines", "dropped_lines"} (kept/dropped = block lines the merge parser keeps / loses).
 Exit 0 always; the caller reads "ok".
 """
 
@@ -40,18 +41,35 @@ def normalize(text: str) -> tuple[str, int]:
     return "\n".join(lines), truncated
 
 
+def dropped_lines(text: str, parsed: dict) -> int:
+    """Block lines the merge parser will not keep (not the number of parser errors).
+
+    With the heading and a block: the non-blank lines of the last block that carry an error. Without the heading,
+    or with no block after it, the parser keeps nothing, so every non-blank line of the last findings-v1 fence in the
+    report is dropped. Block-level notices (several blocks, unclosed block) drop no line by themselves.
+    """
+    found, blocks = fnd._blocks_after(text, fnd._HEAD_FINDINGS, "findings-v1")
+    if found and blocks:
+        body = {ln for ln, raw in blocks[-1][1] if raw.strip()}
+        return len({e["line"] for e in parsed["errors"] if e["line"] in body})
+    _, anywhere = fnd._blocks_after("## Findings block\n" + text, fnd._HEAD_FINDINGS, "findings-v1")
+    return sum(1 for _, raw in anywhere[-1][1] if raw.strip()) if anywhere else 0
+
+
 def main(argv: list[str]) -> int:
     src, out, errs = argv
     try:
         text = open(src, encoding="utf-8").read()
     except OSError as exc:
-        json.dump({"ok": False, "errors": [{"line": 0, "msg": f"cannot read report: {exc}"}], "truncated": 0}, open(errs, "w"))
+        json.dump({"ok": False, "errors": [{"line": 0, "msg": f"cannot read report: {exc}"}], "truncated": 0,
+                   "kept_lines": 0, "dropped_lines": 0}, open(errs, "w"))
         open(out, "w").close()
         return 0
     new, n = normalize(text)
     open(out, "w", encoding="utf-8").write(new)
     parsed = fnd.parse_block(new)
-    json.dump({"ok": parsed["ok"], "errors": parsed["errors"], "truncated": n}, open(errs, "w"))
+    json.dump({"ok": parsed["ok"], "errors": parsed["errors"], "truncated": n, "kept_lines": len(parsed["findings"]) + len(parsed["priors"]),
+               "dropped_lines": dropped_lines(new, parsed)}, open(errs, "w"))
     return 0
 
 
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/bin/claude
old mode 100644
new mode 100755
index 000000000..a0bbf095d
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_h2.py
index 000000000..a1161b3d9 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_h2.py
@@ -82,3 +82,31 @@ def test_no_reask_when_clean(runner):
     runner.plan(f"replay {runner.file(json_reply(report(finding())))}")
     assert runner.run(collab=0).returncode == 0
     assert runner.calls() == 1 and runner.meta()["reask_s"] is None and runner.meta()["dropped_lines"] == 0
+
+
+def test_dropped_counts_lines_not_errors(tmp_path):
+    # one bad line among two: 1 dropped, 1 kept
+    _, e = h2(tmp_path, report(finding(), finding(id="F2", severity="HIGH")))
+    assert e["dropped_lines"] == 1 and e["kept_lines"] == 1
+    # wrong heading: the parser keeps nothing, both block lines are dropped (one line-0 error only)
+    text = report(finding(), finding(id="F2")).replace("## Findings block", "## Findings")
+    _, e = h2(tmp_path, text)
+    assert len(e["errors"]) == 1 and e["dropped_lines"] == 2 and e["kept_lines"] == 0
+    # two blocks: a block-level notice, no dropped line
+    two = report(finding()) + "\n```findings-v1\n" + json.dumps(finding(id="F9")) + "\n```\n"
+    _, e = h2(tmp_path, two)
+    assert not e["ok"] and e["dropped_lines"] == 0 and e["kept_lines"] == 1
+
+
+def test_runner_wrong_heading_reports_all_lines_dropped(runner):
+    text = report(finding(), finding(id="F2")).replace("## Findings block", "## Findings")
+    runner.plan(f"replay {runner.file(json_reply(text))}", f"replay {runner.file(stream_reply(text))}")
+    assert runner.run(collab=0).returncode == 0
+    assert runner.meta()["dropped_lines"] == 2 and runner.calls() == 2
+
+
+def test_reask_with_fewer_kept_lines_is_not_taken(runner):
+    runner.plan(f"replay {runner.file(json_reply(_bad()))}", f"replay {runner.file(stream_reply(report()))}")
+    assert runner.run(collab=0).returncode == 0
+    m = runner.meta()
+    assert m["dropped_lines"] == 1 and len(fnd.parse_block((runner.d / "reviews" / "t2b-1.md").read_text())["findings"]) == 1

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T4.AC1 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:115 anchor="the three tools implement the behaviour of DESIGN.md sections 2.6 and 2.7" chk=y,n,n,n family=h2-dropped-lines fix=count dropped_lines from the block lines that fail (errors with a line number inside the last block's line range); when parse_block fails at block level (heading missing, no block after the heading), count every non-blank line of the block, and do not count the "more than one block" or "not closed" notices as dropped lines first=A1 origin=new covers="Lines still invalid are counted as `dropped_lines` in `meta.json`": `DROPPED=$(jq '.errors|length' h2.json)` counts parser errors, not invalid lines. The runner accepts a report as valid when any line starts with ```findings-v1 (tools/run-reviewer.sh:67), but `parse_block` needs the `## Findings block` heading and otherwise returns one line-0 error and no findings (src/superclaude/cli/review/findings.py:128-133). Probe: a valid-model report with 2 finding lines under `## Findings`, re-ask still the same, gives `valid:true, dropped_lines:1` while the merge parser would keep 0 of the 2 lines. Block-level notices ("more than one findings-v1 block", "not closed", findings.py:143-158) are likewise counted as one dropped line each when no line was dropped. DESIGN.md 6.4 condition 2 reads this field, so the smoke check can pass on a reviewer whose whole block is lost.

Saved-probe re-check hit locations (may be empty): .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:5:"kept_lines", "dropped_lines"} (kept/dropped = block lines the merge parser keeps / loses).
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:44:def dropped_lines(text: str, parsed: dict) -> int:
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:49:    report is dropped. Block-level notices (several blocks, unclosed block) drop no line by themselves.
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:65:                   "kept_lines": 0, "dropped_lines": 0}, open(errs, "w"))
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:72:               "dropped_lines": dropped_lines(new, parsed)}, open(errs, "w"))
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:85:DROPPED=0; REASK_S=null; REASK_TOK=0; REASK_MS=0
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:110:      # (more kept lines wins; on a tie, fewer dropped lines wins)
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:112:           '[$a[0].kept_lines, -$a[0].dropped_lines] >= [$b[0].kept_lines, -$b[0].dropped_lines]' >/dev/null; then
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:117:  DROPPED=$(jq '.dropped_lines' "$OUT/$RID.h2.json")  # block lines the merge parser will not keep
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:131:         dropped_lines:$dr, hang_kill:$hk, valid:$ok, role:$role, collab:$collab, argv:$argv}' "$LAST" > "$OUT/$RID.meta.json"


Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
