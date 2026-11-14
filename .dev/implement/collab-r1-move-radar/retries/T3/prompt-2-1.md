18e8eb6d54a0d71c1c5225866b836a06a0a4f681
Review one task for spec compliance.

Task brief: T3 (source: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/DESIGN.md; task grouping in .dev/implement/collab-r1-move-radar/tasks.md). Covers DESIGN.md section 1.2 rows `tools/radar-classify.jq`, `tools/msg-validate.sh`, `tools/radar-hook.sh`, `tools/settings-gen.sh`, the behaviour of sections 2.2 (message schema and validator), 2.3 (classifier signatures), 2.4 (the radar hook) and 2.5 (item choice and receiver order; the order is computed by `tools/launch.sh --order`, the rest of launch.sh is a later task), and the tests T-3, T-4, T-5, T-6, T-7, T-8, T-9, the settings part of T-10, and the fault-injection tests F-6, F-7, F-14 (tests/test_faults.py; other F tests are added by later tasks). F-13 needs the stub `claude` of the runner task and is not part of T3. Implementation note: the hook reads its frozen per-package inputs (catalogue, index, panel ids and source path) from BOARD/ctx/, which launch.sh will write; the 13 positional hook arguments are as in DESIGN.md 1.2.
T3.AC1: the four tools implement the behaviour of DESIGN.md sections 2.2, 2.3, 2.4 and 2.5.
T3.AC2: T-3, T-4, T-5, T-6, T-7, T-8, T-9, the settings part of T-10, F-6, F-7 and F-14 exist as tests that check what DESIGN.md 6.1/6.2 lists for them, and pass: `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests -q`.
Global constraints: Orchestrator constraints: Create and edit files ONLY under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/ (plus .dev/implement/collab-r1-move-radar/ and scratch under /tmp/evalsb-collab-r1/ and /tmp/collab-r1/). Do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder, or any other redesign's folder. Do not stage, commit or push. Use uv for all Python. Gateway model sessions only under flock /tmp/collab-gateway.lock; models muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7; Opus only as blind judge; never Qwen or glm; NOFALLBACK=1. No full panel runs. Design hard limits: DESIGN.md section 0 'Hard limits carried into every script'.
Start sha: 18e8eb6d54a0d71c1c5225866b836a06a0a4f681
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq
new file mode 100644
index 000000000..866ee22ab
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq
@@ -0,0 +1,58 @@
+# radar-classify.jq: the deterministic classifier (R-31). One tele record in, {"n":..,"sig":[..]} out.
+# Usage: jq -c --slurpfile ix index/<pkg>.json --arg srcpath SB/cand/<pkg>/source.md -f radar-classify.jq
+# Signatures: M1 M2 M4 M7 SRC_OPENED UNNAMED_TEST (never M3 M5 M6 M8 M9 M10). DESIGN.md section 2.3.
+# Input lines may be raw text (jq -R): unparsable lines and lines that are not JSON objects are skipped.
+
+def rec: (if type == "string" then (fromjson? // empty) else . end) | select(type == "object");
+($ix[0]) as $ix
+| ($srcpath | sub("/cand/(?<p>[^/]+)/source\\.md$"; "/\(.p)/repo")) as $repo
+| ($srcpath | capture("/cand/(?<p>[^/]+)/source\\.md$").p // "") as $pkg
+| def norm: tostring | sub("^" + ($repo | gsub("[.]"; "\\.")) + "/?"; "") | sub("^\\./"; "") | if . == "" then "." else . end;
+  def under_tests: . == "tests" or . == "tests/" or startswith("tests/");
+  def is_root: . == "." or . == "./" or . == $repo or . == ($repo + "/");
+  def has_entry: . as $s | any($ix.paths[] , $ix.keys[]; . as $e | $s | contains($e));
+  def unq: if test("^\".*\"$") or test("^'.*'$") then .[1:-1] else . end;
+  # the search segments of a Bash command: text after each grep/egrep/rg up to the next shell separator
+  def segs: [match("\\b(e?grep|rg)\\b([^|;&]*)"; "g") | {tool: .captures[0].string, rest: .captures[1].string}];
+  def toks: [match("\"[^\"]*\"|'[^']*'|[^\\s]+"; "g") | .string];
+  def recursive: .tool == "rg" or (.rest | test("(^|\\s)(-[A-Za-z]*[rR][A-Za-z]*|--recursive)(\\s|$)"));
+  # pattern: first quoted argument, else first token that does not start with -
+  def pattern: (.rest | toks) as $t
+    | (([$t[] | select(test("^[\"']"))] | first) // ([$t[] | select(startswith("-") | not)] | first) // "") | unq;
+  def pathargs: (.rest | toks | map(select(startswith("-") | not))) as $t
+    | (([.rest | toks[] | select(test("^[\"']"))] | first) // ($t | first)) as $pat
+    | ($t | index($pat)) as $i | if $i == null then [] else $t[$i + 1:] | map(unq | norm) end;
+  rec
+  | . as $r
+  | (if ($r.sub // false) then []
+     else
+       ($r.tool) as $tool | ($r.input | if type == "object" then . else {} end) as $in
+       | (if $tool == "Bash" then ($in.command // "" | tostring) else "" end) as $cmd
+       | ($cmd | segs) as $segs
+       | (if $tool == "Grep" then {pat: ($in.pattern // "" | tostring), gpath: (if $in.path then ($in.path | norm) else null end), mode: ($in.output_mode // null)} else null end) as $g
+       | [
+           # M1: recursive grep over tests/ naming a plan path or key
+           (if ($segs | any(recursive and (pathargs | any(under_tests)))) and ($cmd | has_entry) then "M1" else empty end),
+           (if $g and ($g.gpath // "." | under_tests) and ($g.pat | has_entry) then "M1" else empty end),
+           # M2: listing or counting across a directory
+           # (the -l/-c/-L test looks only at the option tokens of each grep segment, never at later commands)
+           (if $tool == "Bash" and (($segs | any(.tool != "rg" and (.rest | toks | any(test("^-[A-Za-z]*[lcL][A-Za-z]*$")))))
+                                    or ($cmd | test("\\bfind\\s|\\|\\s*wc\\s+-l"))) then "M2" else empty end),
+           (if $g and ($g.mode == "files_with_matches" or $g.mode == "count") then "M2" else empty end),
+           # M4: grep whose pattern equals a quoted criterion pattern
+           (if ($segs | any(.tool != "rg" and (pattern as $p | $ix.criterion_greps | index($p) != null))) then "M4" else empty end),
+           (if $g and ($ix.criterion_greps | index($g.pat | unq) != null) then "M4" else empty end),
+           # M7: search from the repository root, or naming a root file
+           (if ($segs | any(recursive and ((pathargs | any(is_root)) or (.tool == "rg" and (pathargs | length) == 0)))) then "M7" else empty end),
+           (if $g and ($g.gpath == null or ($g.gpath | is_root)) then "M7" else empty end),
+           (if ($segs | any(pathargs | any(. as $p | $ix.root_files | index($p) != null)))
+               or ($g and ($g.gpath // "" | . as $p | $ix.root_files | index($p) != null)) then "M7" else empty end),
+           # SRC_OPENED: the package's source.md is read
+           (if ($tool == "Read" and (($in.file_path // "") | tostring | endswith("/cand/" + $pkg + "/source.md")))
+               or ($tool == "Bash" and ($cmd | test("\\b(cat|sed|head|tail|less|nl|awk)\\b")) and ($cmd | contains("cand/" + $pkg + "/source.md")))
+            then "SRC_OPENED" else empty end),
+           # UNNAMED_TEST: a test file the candidate never names
+           (if $tool == "Read" and (($in.file_path // "") | norm | . as $p | (under_tests and ($ix.paths | index($p) == null))) then "UNNAMED_TEST" else empty end)
+         ] | unique
+     end) as $sig
+  | {n: $r.n, sig: $sig}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/msg-validate.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/msg-validate.sh
new file mode 100644
index 000000000..dda814df2
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/msg-validate.sh
@@ -0,0 +1,45 @@
+#!/usr/bin/env bash
+# msg-validate.sh <catalogue.json> <searcher rid> <reader rid,reader rid>
+# panel-msg/1 validator, F3 subset (R-06, R-08, leak lookup). stdin: one envelope per line,
+# {"line":"<serialised board line>","text":"<rendered text>"}. Valid board lines go to stdout, rejects to stderr as
+# {"reject":"<reason>","line":..}. Exit 0 when every line is valid, 1 otherwise. DESIGN.md section 2.2.
+set -u -o pipefail
+CAT=${1:?usage: msg-validate.sh <catalogue.json> <searcher rid> <reader rids comma list>}; SEARCHER=${2:?}; READERS=${3:?}
+rc=0
+while IFS= read -r env || [ -n "$env" ]; do
+  out=$(printf '%s' "$env" | jq -R -r -c --slurpfile cat "$CAT" --arg s "$SEARCHER" --arg r "$READERS" '
+    ($cat[0]) as $c | ([$s] + ($r | split(","))) as $ids
+    | (try fromjson catch null) as $e
+    | if ($e | type) != "object" or ($e.line | type) != "string" then ["REJ", {reject: "not_json", line: .}]
+      else ($e.line) as $l | ($e.text // null) as $text
+      | if ($l | utf8bytelength) > 600 then ["REJ", {reject: "too_long", line: $l}]
+        else (try ($l | fromjson) catch null) as $m
+        | if ($m | type) != "object" then ["REJ", {reject: "not_json", line: $l}]
+          else ([$m | keys[] | select(IN("v", "id", "run", "from", "to", "t", "kind", "move") | not)] | first) as $bk
+          | if $bk then ["REJ", {reject: "bad_key:\($bk)", line: $l}]
+            else ([
+                (if $m.v != "panel-msg/1" then "v" else empty end),
+                (if ($m.id | type) != "string" then "id" else empty end),
+                (if ($m.run | type) != "string" then "run" else empty end),
+                (if $m.from != "radar" then "from" else empty end),
+                (if ($ids | index($m.to)) == null then "to" else empty end),
+                (if ($m.t | type) != "number" or ($m.t | floor) != $m.t then "t" else empty end),
+                (if $m.kind != "move" then "kind" else empty end)] | first) as $bf
+            | if $bf then ["REJ", {reject: "bad_field:\($bf)", line: $l}]
+              elif ($m | has("move")) and (($m.move | type) != "string" or ($m.move | test("^M([1-9]|10)$") | not)) then ["REJ", {reject: "bad_move", line: $l}]
+              else (if ($m | has("move")) | not then $c.src_text
+                    elif ($c.observable | index($m.move)) != null and $m.to == $s then $c.moves[$m.move] + $c.observable_suffix
+                    else $c.moves[$m.move] end) as $want
+              | if $text != $want then ["REJ", {reject: "leak", line: $l}] else ["OK", $l] end
+              end
+            end
+          end
+        end
+      end
+    | if .[0] == "OK" then "OK\t\(.[1])" else "REJ\t\(.[1] | tojson)" end' 2>/dev/null) || out="REJ	{\"reject\":\"not_json\",\"line\":null}"
+  case $out in
+    OK$'\t'*) printf '%s\n' "${out#OK$'\t'}";;
+    *) printf '%s\n' "${out#REJ$'\t'}" >&2; rc=1;;
+  esac
+done
+exit $rc
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-hook.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-hook.sh
new file mode 100644
index 000000000..8c1465e74
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-hook.sh
@@ -0,0 +1,120 @@
+#!/usr/bin/env bash
+# radar-hook.sh <BOARD> <RUN> <RID> <ROLE> <T0_MS> <FINISH_MS> <GUARD_MS> <K> <CP1> <CP2> <ORDER> <PKG> <CLOCK_FILE>
+# The PostToolUse hook of F3 (DESIGN.md section 2.4): telemetry, checkpoint logic, seal, injection, finish signal.
+# Frozen per-package inputs are read from BOARD/ctx/ (written by launch.sh): catalogue.json, index.json and
+# panel.json = {"searcher":rid,"readers":[rid,rid],"srcpath":".../cand/<pkg>/source.md"}.
+# Prints nothing or one {"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":..}}; always exits 0.
+BOARD=${1:-}; RUN=${2:-}; RID=${3:-}; ROLE=${4:-}; T0_MS=${5:-0}; FINISH_MS=${6:-0}; GUARD_MS=${7:-0}
+K=${8:-0}; CP1=${9:-0}; CP2=${10:-0}; ORDER=${11:-}; PKG=${12:-}; CLOCK_FILE=${13:-}
+TOOLS=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
+MET=$BOARD/metrics/$RID.jsonl
+start_ms=$(date +%s%3N)
+now_ms() { if [ -n "$CLOCK_FILE" ]; then tr -dc '0-9' < "$CLOCK_FILE"; else date +%s%3N; fi; }
+logm() { printf '%s\n' "$1" >> "$MET"; }
+
+main() {
+  set -eu -o pipefail
+  local in now n tele ix cat panel sealed inj eligible item move text slot hint line env valid
+  in=$(head -c 1048576)
+  printf '%s' "$in" | jq -e 'type == "object"' >/dev/null      # not JSON -> error -> hook_error
+  now=$(now_ms); [ -n "$now" ]
+  mkdir -p "$BOARD/tele" "$BOARD/state" "$BOARD/metrics"
+  exec 9>>"$BOARD/state/$RID.lock"; flock -w 4 9
+  # 3. subagent call: log only, never counted or classified
+  if [ "$(printf '%s' "$in" | jq -r '.agent_id // empty')" != "" ]; then
+    tele=$(printf '%s' "$in" | jq -c --argjson t "$now" --arg rid "$RID" \
+      '{n: null, t: $t, rid: $rid, sub: true, tool: .tool_name, input: (.tool_input // {} | walk(if type == "string" then .[:2000] else . end))}')
+    printf '%s\n' "$tele" >> "$BOARD/tele/$RID.jsonl"; return 0
+  fi
+  # 4. count and telemetry (one O_APPEND write)
+  n=$(( $(cat "$BOARD/state/$RID.count" 2>/dev/null || echo 0) + 1 )); echo "$n" > "$BOARD/state/$RID.count"
+  N=$n
+  tele=$(printf '%s' "$in" | jq -c --argjson n "$n" --argjson t "$now" --arg rid "$RID" \
+    '{n: $n, t: $t, rid: $rid, sub: false, tool: .tool_name, input: (.tool_input // {} | walk(if type == "string" then .[:2000] else . end))}')
+  printf '%s\n' "$tele" >> "$BOARD/tele/$RID.jsonl"
+  sealed=$(cat "$BOARD/state/$RID.sealed" 2>/dev/null || true)
+  [ "$sealed" = failed ] && return 0                              # a failed seal: nothing more is delivered
+  cat=$BOARD/ctx/catalogue.json
+  # 5. finish signal; after FINISH_MS nothing else is ever injected
+  if [ "$now" -ge "$FINISH_MS" ]; then
+    [ -e "$BOARD/state/$RID.finish" ] && return 0
+    : > "$BOARD/state/$RID.finish"
+    logm "{\"ev\":\"finish\",\"t\":$now,\"n\":$n}"
+    jq -c '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: .finish_text}}' "$cat"
+    return 0
+  fi
+  # 6. checkpoint test
+  eligible=$( [ "$K" -ge 1 ] && echo "$CP1"; [ "$K" -ge 2 ] && echo "$CP2"; true )
+  grep -qx -- "$n" <<< "$eligible" || return 0      # here-strings, not pipes: grep -q must not SIGPIPE a writer
+  inj=$(grep -c '"ev":"inject"' "$MET" 2>/dev/null || true)
+  [ "${inj:-0}" -ge "$K" ] && return 0
+  if [ "$now" -ge "$GUARD_MS" ]; then logm "{\"ev\":\"skip\",\"reason\":\"guard\",\"n\":$n}"; return 0; fi
+  # 7. seal (fail closed)
+  if [ -z "$sealed" ]; then
+    local tp; tp=$(printf '%s' "$in" | jq -r '.transcript_path // empty')
+    mkdir -p "$BOARD/snap"
+    if [ -n "$tp" ] && cp "$tp" "$BOARD/snap/$RID.jsonl" 2>/dev/null \
+       && (cd "$BOARD/snap" && sha256sum "$RID.jsonl" > "$RID.sha256"); then
+      logm "{\"ev\":\"seal\",\"t\":$now,\"sha256\":\"$(cut -d' ' -f1 "$BOARD/snap/$RID.sha256")\"}"
+      echo ok > "$BOARD/state/$RID.sealed"
+    else
+      echo failed > "$BOARD/state/$RID.sealed"
+      logm "{\"ev\":\"snapshot_missing\",\"t\":$now}"
+      return 0
+    fi
+  fi
+  # 8. choose the item (section 2.5)
+  ix=$BOARD/ctx/index.json; panel=$BOARD/ctx/panel.json
+  local srcpath; srcpath=$(jq -r .srcpath "$panel")
+  classify() { jq -R -c --slurpfile ix "$ix" --arg srcpath "$srcpath" -f "$TOOLS/radar-classify.jq" "$@" | jq -r '.sig[]'; }
+  local injected; injected=$(jq -R -r 'fromjson? // empty | select(type == "object" and .ev == "inject") | .move // "SRC"' "$MET" 2>/dev/null || true)
+  item=""
+  local own=""; [ "$n" = "$CP1" ] && own=$(classify "$BOARD/tele/$RID.jsonl")
+  if [ "$n" = "$CP1" ] && ! grep -qx SRC_OPENED <<< "$own"; then
+    item=SRC
+  else
+    local covered=""
+    [ "$ROLE" = searcher ] && covered=$(cat "$BOARD"/tele/*.jsonl | classify | sort -u)
+    for move in ${ORDER//,/ }; do
+      grep -qx -- "$move" <<< "$injected" && continue
+      [ "$ROLE" = searcher ] && grep -qx -- "$move" <<< "$covered" && continue
+      item=$move; break
+    done
+  fi
+  if [ -z "$item" ]; then logm "{\"ev\":\"skip\",\"reason\":\"no_gap\",\"n\":$n}"; return 0; fi
+  # 9. task hint (metrics only, never in the message)
+  hint=$(printf '%s' "$in" | jq -c --slurpfile ix "$ix" '(.tool_input // {} | tostring) as $s
+      | [$ix[0].task_of_path | to_entries[] | select(.key as $k | $s | contains($k)) | .value[]] | unique')
+  # 10. line, validation, delivery
+  local id; id=$(printf 'm-%s-%02d' "$RID" "$n")
+  if [ "$item" = SRC ]; then
+    move=null; slot=src; text=$(jq -r .src_text "$cat")
+    line=$(jq -n -c --arg id "$id" --arg run "$RUN" --arg to "$RID" --argjson t "$now" '{v:"panel-msg/1",id:$id,run:$run,from:"radar",to:$to,t:$t,kind:"move"}')
+  else
+    move="\"$item\""
+    if [ "$ROLE" = searcher ]; then slot=search; else slot=static; fi
+    text=$(jq -r --arg m "$item" --arg role "$ROLE" '.moves[$m] + (if $role == "searcher" and (.observable | index($m)) != null then .observable_suffix else "" end)' "$cat")
+    line=$(jq -n -c --arg id "$id" --arg run "$RUN" --arg to "$RID" --argjson t "$now" --arg m "$item" '{v:"panel-msg/1",id:$id,run:$run,from:"radar",to:$to,t:$t,kind:"move",move:$m}')
+  fi
+  env=$(jq -n -c --arg line "$line" --arg text "$text" '{line:$line,text:$text}')
+  valid=$(printf '%s\n' "$env" | bash "$TOOLS/msg-validate.sh" "$cat" "$(jq -r .searcher "$panel")" "$(jq -r '.readers|join(",")' "$panel")" 2>/dev/null) \
+    || { logm "{\"ev\":\"hook_error\",\"t\":$now,\"msg\":\"validator rejected $id\"}"; return 0; }
+  mkdir -p "$BOARD/msgs"
+  printf '%s\n' "$valid" >> "$BOARD/msgs/radar.jsonl"
+  logm "$(jq -n -c --arg id "$id" --argjson t "$now" --argjson n "$n" --argjson move "$move" --arg slot "$slot" \
+      --argjson hint "$hint" --arg text "$text" --arg sha "$(printf '%s' "$text" | sha256sum | cut -d' ' -f1)" \
+      '{ev:"inject",id:$id,t:$t,n:$n,move:$move,slot_type:$slot,task_hint:$hint,text:$text,text_sha256:$sha}')"
+  jq -n -c --arg text "$text" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $text}}'
+}
+
+N=null
+mkdir -p "$BOARD/metrics" 2>/dev/null
+out=$(main); rc=$?
+if [ $rc -eq 0 ]; then
+  [ -n "$out" ] && printf '%s\n' "$out"
+else
+  printf '{"ev":"hook_error","t":%s,"msg":"rc=%s"}\n' "$(date +%s%3N)" "$rc" >> "$MET" 2>/dev/null
+fi
+[ -f "$BOARD/state/$RID.count" ] && N=$(cat "$BOARD/state/$RID.count" 2>/dev/null)
+printf '{"ev":"t","n":%s,"ms":%s}\n' "${N:-null}" "$(( $(date +%s%3N) - start_ms ))" >> "$MET" 2>/dev/null
+exit 0
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/settings-gen.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/settings-gen.sh
new file mode 100644
index 000000000..1ac4f6ab2
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/settings-gen.sh
@@ -0,0 +1,14 @@
+#!/usr/bin/env bash
+# settings-gen.sh <BOARD> <RUN> <RID> <ROLE> <T0_MS> <FINISH_MS> <GUARD_MS> <K> <CP1> <CP2> <ORDER> <PKG> <CLOCK_FILE>
+# Prints the per-reviewer --settings JSON (R-21): one PostToolUse handler, matcher "*", timeout 5, every value
+# single-quoted and baked into the command string. Refuses (exit 2) a value containing a quote, a $ or a newline.
+set -u -o pipefail
+[ $# -eq 13 ] || { echo "usage: settings-gen.sh <13 hook arguments>" >&2; exit 2; }
+HOOK=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/radar-hook.sh
+CMD="bash $HOOK"
+for v in "$@"; do
+  case $v in *"'"*|*'$'*|*$'\n'*|*'`'*|*'\'*) echo "REFUSE unsafe value: $v" >&2; exit 2;; esac
+  CMD="$CMD '$v'"
+done
+case $CMD in *'$'*) echo "REFUSE \$ in command" >&2; exit 2;; esac
+jq -n -c --arg cmd "$CMD" '{hooks: {PostToolUse: [{matcher: "*", hooks: [{type: "command", command: $cmd, timeout: 5}]}]}}'
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh
new file mode 100644
index 000000000..bc8f39128
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh
@@ -0,0 +1,12 @@
+#!/usr/bin/env bash
+# launch.sh: PANEL_COLLAB=<0|1> bash tools/launch.sh <panel> <rep> [<pkg> ...]   (DESIGN.md section 5)
+#            bash tools/launch.sh --order <rid> <searcher|reader>   (prints the receiver's move order, section 2.5)
+set -u -o pipefail
+order() { # rotate the role list left by int(sha256(rid)[0:8], 16) mod len
+  local rid=$1 role=$2 list h off i out=()
+  if [ "$role" = searcher ]; then list=(M1 M2 M7 M4); else list=(M3 M5 M6 M9 M8 M10); fi
+  h=$(printf %s "$rid" | sha256sum | cut -c1-8); off=$(( 16#$h % ${#list[@]} ))
+  for ((i = 0; i < ${#list[@]}; i++)); do out+=("${list[(i + off) % ${#list[@]}]}"); done
+  (IFS=,; echo "${out[*]}")
+}
+if [ "${1:-}" = --order ]; then order "$2" "$3"; exit 0; fi
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
deleted file mode 100644
index f97723d1a..000000000
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
+++ /dev/null
@@ -1,60 +0,0 @@
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
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
index 000000000..45ddedcd9 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
@@ -58,3 +58,93 @@ def jload(p):
 @pytest.fixture
 def clean_env():
     return {k: v for k, v in os.environ.items()}
+
+
+# ---------------------------------------------------------------- hook kit
+SEARCHER, READERS = "t2b-1", ["t4-1", "t3-1"]
+CAT = jload(R1 / "config" / "catalogue.json")
+ORDERS = {"t2b-1": "M2,M7,M4,M1", "t4-1": "M3,M5,M6,M9,M8,M10", "t3-1": "M8,M10,M3,M5,M6,M9",
+          "t1b-1": "M7,M4,M1,M2", "t2-1": "M1,M2,M7,M4"}
+
+
+class Board:
+    """A board under tmp_path with ctx/ files, a clock file and a transcript, driven call by call."""
+
+    def __init__(self, tmp_path, sb="/tmp/sbX"):
+        self.dir = tmp_path / "board"
+        (self.dir / "ctx").mkdir(parents=True)
+        shutil.copy(R1 / "config" / "catalogue.json", self.dir / "ctx" / "catalogue.json")
+        shutil.copy(FIX / "index.json", self.dir / "ctx" / "index.json")
+        self.repo = f"{sb}/{PKG}/repo"
+        self.src = f"{sb}/cand/{PKG}/source.md"
+        (self.dir / "ctx" / "panel.json").write_text(json.dumps({"searcher": SEARCHER, "readers": READERS, "srcpath": self.src}))
+        self.clock = tmp_path / "clock"
+        self.set_clock(1000)
+        self.transcript = tmp_path / "transcript.jsonl"
+        self.transcript.write_text('{"type":"user"}\n{"type":"assistant"}\n')
+
+    def set_clock(self, ms):
+        self.clock.write_text(str(ms))
+
+    def stdin(self, tool="Bash", inp=None, agent_id=None, transcript=None):
+        d = {"session_id": "s1", "transcript_path": str(transcript or self.transcript), "hook_event_name": "PostToolUse",
+             "tool_name": tool, "tool_input": inp if inp is not None else {"command": "ls"}, "tool_response": {}}
+        if agent_id:
+            d["agent_id"] = agent_id
+        return json.dumps(d)
+
+    def args(self, rid, role, k=2, cps=None, finish=10**9, guard=10**9, order=None):
+        cps = cps or ((6, 10) if role == "searcher" else (8, 12))
+        return [str(self.dir), "row-c1-r0/" + PKG, rid, role, "0", str(finish), str(guard), str(k), str(cps[0]),
+                str(cps[1]), order or ORDERS[rid], PKG, str(self.clock)]
+
+    def call(self, rid, role, env=None, raw_stdin=None, **kw):
+        a = self.args(rid, role, **{k: v for k, v in kw.items() if k in ("k", "cps", "finish", "guard", "order")})
+        s = raw_stdin if raw_stdin is not None else self.stdin(**{k: v for k, v in kw.items() if k in ("tool", "inp", "agent_id", "transcript")})
+        r = run(["bash", str(TOOLS / "radar-hook.sh"), *a], stdin=s, env=env)
+        assert r.returncode == 0, r.stderr
+        return r.stdout.strip()
+
+    def metrics(self, rid):
+        p = self.dir / "metrics" / f"{rid}.jsonl"
+        return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
+
+    def metrics_safe(self, rid):
+        """Metrics lines that are JSON objects (a test may plant junk lines)."""
+        p = self.dir / "metrics" / f"{rid}.jsonl"
+        out = []
+        for x in p.read_text().splitlines() if p.exists() else []:
+            try:
+                v = json.loads(x)
+            except ValueError:
+                continue
+            if isinstance(v, dict):
+                out.append(v)
+        return out
+
+    def events(self, rid, ev):
+        return [m for m in self.metrics(rid) if m.get("ev") == ev]
+
+    def tele(self, rid, line):
+        p = self.dir / "tele" / f"{rid}.jsonl"
+        p.parent.mkdir(exist_ok=True)
+        with p.open("a") as f:
+            f.write(line + "\n")
+
+
+def expected_text(move, role):
+    if move is None:
+        return CAT["src_text"]
+    return CAT["moves"][move] + (CAT["observable_suffix"] if role == "searcher" and move in CAT["observable"] else "")
+
+
+def ctx_text(out):
+    d = json.loads(out)
+    assert list(d) == ["hookSpecificOutput"] and d["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
+    assert set(d["hookSpecificOutput"]) == {"hookEventName", "additionalContext"}
+    return d["hookSpecificOutput"]["additionalContext"]
+
+
+@pytest.fixture
+def board(tmp_path):
+    return Board(tmp_path)
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/index.json b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/index.json
new file mode 100644
index 000000000..12ef72248
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/index.json
@@ -0,0 +1,4 @@
+{"paths":["src/app/merge_guard.py","src/app/core.py","tests/app/test_core.py","docs/guide.md","CHANGELOG.md"],
+ "keys":["merge_guard","core","test_core","guide","CHANGELOG"],
+ "task_of_path":{"src/app/merge_guard.py":["T1"],"src/app/core.py":["T1"],"docs/guide.md":["T2"],"tests/app/test_core.py":["T3"]},
+ "tasks":["T1","T2","T3"],"criterion_greps":["merge_guard","HOW-WE-WORK"],"root_files":["CHANGELOG.md","Makefile"]}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_classify.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_classify.py
new file mode 100644
index 000000000..e0e5fef4c
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_classify.py
@@ -0,0 +1,78 @@
+"""T-3: radar-classify.jq signatures, negatives and the never-unobservable property."""
+
+import json
+
+import pytest
+from conftest import FIX, PKG, TOOLS, run
+
+SB = "/tmp/sbX"
+REPO = f"{SB}/{PKG}/repo"
+SRC = f"{SB}/cand/{PKG}/source.md"
+
+
+def classify(records):
+    lines = "\n".join(json.dumps(r) for r in records) + "\n"
+    r = run(["jq", "-R", "-c", "--slurpfile", "ix", str(FIX / "index.json"), "--arg", "srcpath", SRC,
+             "-f", str(TOOLS / "radar-classify.jq")], stdin=lines)
+    assert r.returncode == 0, r.stderr
+    return [json.loads(x)["sig"] for x in r.stdout.splitlines()]
+
+
+def bash(cmd):
+    return {"n": 1, "t": 0, "rid": "x", "sub": False, "tool": "Bash", "input": {"command": cmd}}
+
+
+def tool(name, **inp):
+    return {"n": 1, "t": 0, "rid": "x", "sub": False, "tool": name, "input": inp}
+
+
+POS = [
+    ("M1", bash("grep -rn merge_guard tests/")),
+    ("M1", tool("Grep", pattern="merge_guard", path=f"{REPO}/tests")),
+    ("M2", bash("grep -l x src/")),
+    ("M2", bash("ls docs | wc -l")),
+    ("M2", tool("Grep", pattern="x", path="src", output_mode="count")),
+    ("M4", bash('grep -n "HOW-WE-WORK" docs/guide.md')),
+    ("M4", bash("grep -n HOW-WE-WORK docs/guide.md")),
+    ("M7", bash("grep -rn 43 .")),
+    ("M7", tool("Grep", pattern="43")),
+    ("M7", bash("grep 43 CHANGELOG.md")),
+    ("SRC_OPENED", tool("Read", file_path=SRC)),
+    ("SRC_OPENED", bash(f"sed -n 1,80p {SRC}")),
+    ("UNNAMED_TEST", tool("Read", file_path=f"{REPO}/tests/x/test_y.py")),
+]
+NEG = [
+    ("M1", bash("grep -rn merge_guard src/")),
+    ("M1", bash("grep -rn unrelated_word tests/")),
+    ("UNNAMED_TEST", tool("Read", file_path=f"{REPO}/tests/app/test_core.py")),
+    ("M4", bash('grep -n "HOW-WE-WOR" docs/guide.md')),
+    ("M2", bash("grep -rn x src/ | head -c 500")),
+    ("M2", bash("grep -n x f; ls -la")),
+    ("M2", bash("grep -n x f && sort -c f")),
+]
+
+
+@pytest.mark.parametrize("sig,rec", POS, ids=[f"{s}-{i}" for i, (s, _) in enumerate(POS)])
+def test_positive(sig, rec):
+    assert sig in classify([rec])[0]
+
+
+@pytest.mark.parametrize("sig,rec", NEG, ids=[f"not-{s}-{i}" for i, (s, _) in enumerate(NEG)])
+def test_negative(sig, rec):
+    assert sig not in classify([rec])[0]
+
+
+def test_sub_records_never_counted():
+    rec = dict(bash("grep -rn merge_guard tests/"), sub=True)
+    assert classify([rec]) == [[]]
+
+
+def test_corrupt_line_skipped():
+    r = run(["jq", "-R", "-c", "--slurpfile", "ix", str(FIX / "index.json"), "--arg", "srcpath", SRC,
+             "-f", str(TOOLS / "radar-classify.jq")], stdin='{"n":1,"tool":"Ba\n' + json.dumps(bash("grep -l x src/")) + "\n")
+    assert r.returncode == 0 and [json.loads(x)["sig"] for x in r.stdout.splitlines()] == [["M2"]]
+
+
+def test_never_emits_unobservable_moves():
+    out = classify([r for _, r in POS + NEG])
+    assert all(s not in {"M3", "M5", "M6", "M8", "M9", "M10"} for sigs in out for s in sigs)
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_order.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_order.py
new file mode 100644
index 000000000..1d5007dbc
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_order.py
@@ -0,0 +1,22 @@
+"""T-4: receiver order is a rotation by sha256(rid)[0:8] mod len."""
+
+from conftest import TOOLS, run
+
+
+def order(rid, role):
+    r = run(["bash", str(TOOLS / "launch.sh"), "--order", rid, role])
+    assert r.returncode == 0, r.stderr
+    return r.stdout.strip().split(",")
+
+
+def test_offsets():
+    assert order("t4-1", "reader") == ["M3", "M5", "M6", "M9", "M8", "M10"]  # offset 0
+    assert order("t3-1", "reader") == ["M8", "M10", "M3", "M5", "M6", "M9"]  # offset 4
+    assert order("t2b-1", "searcher") == ["M2", "M7", "M4", "M1"]  # offset 1
+    assert order("t1b-1", "searcher") == ["M7", "M4", "M1", "M2"]  # offset 2
+    assert order("t2-1", "searcher") == ["M1", "M2", "M7", "M4"]  # offset 0
+
+
+def test_lunas_differ_at_both_checkpoints():
+    a, b = order("t4-1", "reader"), order("t3-1", "reader")
+    assert a[0] != b[0] and a[1] != b[1]
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_schedule.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_schedule.py
new file mode 100644
index 000000000..e6fb00b7e
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_schedule.py
@@ -0,0 +1,76 @@
+"""T-5: checkpoint schedule, source.md check, peer coverage, guard, output shape and text."""
+
+import json
+
+from conftest import ctx_text, expected_text
+
+
+def drive(board, rid, role, calls, **kw):
+    outs = {}
+    for i in range(1, calls + 1):
+        o = board.call(rid, role, **kw)
+        if o:
+            outs[i] = o
+    return outs
+
+
+def read_src(board, rid, role, **kw):
+    return board.call(rid, role, tool="Read", inp={"file_path": board.src}, **kw)
+
+
+def test_searcher_k2_injects_at_6_and_10_only(board):
+    outs = drive(board, "t2b-1", "searcher", 14)
+    assert sorted(outs) == [6, 10]
+    assert ctx_text(outs[6]) == expected_text(None, "searcher")  # no SRC_OPENED -> the source.md check first
+    assert ctx_text(outs[10]) == expected_text("M2", "searcher")  # first of the order, with the suffix
+    inj = board.events("t2b-1", "inject")
+    assert len(inj) == 2 and inj[0]["slot_type"] == "src" and inj[0]["move"] is None
+    assert inj[1]["slot_type"] == "search" and inj[1]["move"] == "M2"
+
+
+def test_searcher_k1_injects_at_6_only(board):
+    assert sorted(drive(board, "t2b-1", "searcher", 14, k=1)) == [6]
+
+
+def test_reader_injects_at_8_and_12_without_suffix(board):
+    read_src(board, "t4-1", "reader")
+    outs = drive(board, "t4-1", "reader", 13)
+    assert sorted(outs) == [7, 11]  # one call was the Read, so the counted calls 8 and 12 are loop steps 7 and 11
+    assert ctx_text(outs[7]) == expected_text("M3", "reader")
+    assert ctx_text(outs[11]) == expected_text("M5", "reader")
+    assert all("No panel member" not in ctx_text(o) for o in outs.values())
+    assert [e["slot_type"] for e in board.events("t4-1", "inject")] == ["static", "static"]
+
+
+def test_source_check_not_sent_when_opened(board):
+    read_src(board, "t2b-1", "searcher")
+    outs = drive(board, "t2b-1", "searcher", 9)
+    assert ctx_text(outs[5]) == expected_text("M2", "searcher")
+
+
+def test_peer_coverage_skips_move(board):
+    board.tele("t4-1", json.dumps({"n": 1, "t": 0, "rid": "t4-1", "sub": False, "tool": "Bash", "input": {"command": "grep -c x src/"}}))
+    read_src(board, "t2b-1", "searcher")
+    outs = drive(board, "t2b-1", "searcher", 5)
+    assert ctx_text(outs[5]) == expected_text("M7", "searcher")  # M2 covered by a peer -> next uncovered
+
+
+def test_all_covered_is_no_gap(board):
+    for c in ("grep -c x src/", "grep -rn x .", "grep -n HOW-WE-WORK docs/guide.md", "grep -rn merge_guard tests/"):
+        board.tele("t3-1", json.dumps({"n": 1, "t": 0, "rid": "t3-1", "sub": False, "tool": "Bash", "input": {"command": c}}))
+    read_src(board, "t2b-1", "searcher")
+    outs = drive(board, "t2b-1", "searcher", 9)
+    assert outs == {}
+    assert [e["reason"] for e in board.events("t2b-1", "skip")] == ["no_gap", "no_gap"]
+    assert board.events("t2b-1", "inject") == []
+
+
+def test_no_injection_at_or_after_guard(board):
+    board.set_clock(5000)
+    outs = drive(board, "t2b-1", "searcher", 12, guard=5000)
+    assert outs == {} and [e["reason"] for e in board.events("t2b-1", "skip")] == ["guard", "guard"]
+
+
+def test_at_most_k_injections(board):
+    drive(board, "t2b-1", "searcher", 30)
+    assert len(board.events("t2b-1", "inject")) == 2
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_finish.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_finish.py
new file mode 100644
index 000000000..3a4b51d48
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_finish.py
@@ -0,0 +1,14 @@
+"""T-6: the finish signal (R-41)."""
+
+from conftest import CAT, ctx_text
+
+
+def test_finish_once_and_nothing_after(board):
+    for _ in range(4):
+        board.call("t2b-1", "searcher")
+    board.set_clock(2000)
+    outs = [board.call("t2b-1", "searcher", finish=2000) for _ in range(10)]  # calls 5..14 include checkpoints 6 and 10
+    assert ctx_text(outs[0]) == CAT["finish_text"]
+    assert all(o == "" for o in outs[1:])
+    assert len(board.events("t2b-1", "finish")) == 1
+    assert board.events("t2b-1", "inject") == []
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_seal.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_seal.py
new file mode 100644
index 000000000..3cde385aa
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_seal.py
@@ -0,0 +1,26 @@
+"""T-7: seal before the first delivery; fail closed on an unreadable transcript (R-10)."""
+
+import hashlib
+
+from conftest import ctx_text
+
+
+def test_seal_written_before_inject(board):
+    for i in range(6):
+        out = board.call("t2b-1", "searcher")
+    assert ctx_text(out)
+    snap = board.dir / "snap" / "t2b-1.jsonl"
+    assert snap.read_bytes() == board.transcript.read_bytes()
+    sha = hashlib.sha256(snap.read_bytes()).hexdigest()
+    assert (board.dir / "snap" / "t2b-1.sha256").read_text().split()[0] == sha
+    evs = [m["ev"] for m in board.metrics("t2b-1") if m["ev"] in ("seal", "inject")]
+    assert evs == ["seal", "inject"]
+    assert board.events("t2b-1", "seal")[0]["sha256"] == sha
+
+
+def test_unreadable_transcript_fails_closed(board, tmp_path):
+    outs = [board.call("t2b-1", "searcher", transcript=tmp_path / "missing.jsonl") for _ in range(12)]
+    assert all(o == "" for o in outs)  # nothing at checkpoint 6 nor at 10
+    assert len(board.events("t2b-1", "snapshot_missing")) == 1
+    assert board.events("t2b-1", "inject") == []
+    assert (board.dir / "state" / "t2b-1.sealed").read_text().strip() == "failed"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_errors.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_errors.py
new file mode 100644
index 000000000..48110541b
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_errors.py
@@ -0,0 +1,54 @@
+"""T-8: the hook never breaks a review (R-22)."""
+
+import os
+
+from conftest import ctx_text
+
+
+def test_corrupt_peer_line(board):
+    board.tele("t4-1", '{"n":1,"tool":"Bash","inp')
+    outs = [board.call("t2b-1", "searcher") for _ in range(6)]
+    assert ctx_text(outs[5])
+
+
+def test_non_object_json_lines_skipped(board):
+    # lines that parse but are not objects, last in the peer file and in the metrics file
+    for junk in ("[1]", "42", '"x"', '{"n":1,"tool":"Bash","input":"not an object"}'):
+        board.tele("t4-1", junk)
+    outs = [board.call("t2b-1", "searcher") for _ in range(10)]
+    with (board.dir / "metrics" / "t2b-1.jsonl").open("a") as f:
+        f.write("[1]\n")
+    board.call("t2b-1", "searcher")
+    assert ctx_text(outs[5]) and ctx_text(outs[9])
+    assert not [m for m in board.metrics_safe("t2b-1") if m.get("ev") == "hook_error"]
+    assert len([m for m in board.metrics_safe("t2b-1") if m.get("ev") == "inject"]) == 2
+
+
+def test_unwritable_msgs(board):
+    (board.dir / "msgs").mkdir()
+    os.chmod(board.dir / "msgs", 0o500)
+    try:
+        outs = [board.call("t2b-1", "searcher") for _ in range(6)]
+    finally:
+        os.chmod(board.dir / "msgs", 0o700)
+    assert all(o == "" for o in outs)
+    assert len(board.events("t2b-1", "hook_error")) == 1
+
+
+def test_stdin_not_json(board):
+    assert board.call("t2b-1", "searcher", raw_stdin="not json at all") == ""
+    assert len(board.events("t2b-1", "hook_error")) == 1
+
+
+def test_timing_event_on_every_exit(board):
+    for _ in range(3):
+        board.call("t2b-1", "searcher")
+    ts = board.events("t2b-1", "t")
+    assert len(ts) == 3 and all(isinstance(t["ms"], int) for t in ts)
+
+
+def test_subagent_calls_logged_not_counted(board):
+    for _ in range(6):
+        board.call("t2b-1", "searcher", agent_id="agent-1")
+    assert not (board.dir / "state" / "t2b-1.count").exists()
+    assert board.events("t2b-1", "inject") == []
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_validate.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_validate.py
new file mode 100644
index 000000000..0187e8ae3
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_validate.py
@@ -0,0 +1,56 @@
+"""T-9: msg-validate.sh accepts radar lines and rejects with the right reason."""
+
+import json
+
+import pytest
+from conftest import CAT, R1, TOOLS, run
+
+BASE = {"v": "panel-msg/1", "id": "m-t4-1-08", "run": "el2-c1-r3/P", "from": "radar", "to": "t4-1", "t": 1763062000123, "kind": "move"}
+
+
+def validate(line, text):
+    env = json.dumps({"line": line if isinstance(line, str) else json.dumps(line), "text": text})
+    r = run(["bash", str(TOOLS / "msg-validate.sh"), str(R1 / "config" / "catalogue.json"), "t2b-1", "t4-1,t3-1"], stdin=env + "\n")
+    rej = [json.loads(x)["reject"] for x in r.stderr.splitlines()]
+    return r.returncode, r.stdout.strip(), rej
+
+
+def test_accepts_move_and_src_check():
+    assert validate(dict(BASE, move="M5"), CAT["moves"]["M5"])[0] == 0
+    rc, out, _ = validate(BASE, CAT["src_text"])
+    assert rc == 0 and json.loads(out) == BASE
+    assert validate(dict(BASE, to="t2b-1", move="M2"), CAT["moves"]["M2"] + CAT["observable_suffix"])[0] == 0
+
+
+def test_too_long():
+    short = json.dumps(dict(BASE, move="M5"))
+    line = json.dumps(dict(BASE, move="M5", run=BASE["run"] + "x" * (601 - len(short))))
+    assert len(line.encode()) == 601
+    assert validate(line, CAT["moves"]["M5"])[2] == ["too_long"]
+    ok = json.dumps(dict(BASE, move="M5", run=BASE["run"] + "x" * (600 - len(short))))
+    assert len(ok.encode()) == 600 and validate(ok, CAT["moves"]["M5"])[0] == 0
+
+
+@pytest.mark.parametrize("key", ["claim", "verdict", "blocking", "severity", "category", "note", "anchor", "items", "extra"])
+def test_bad_key(key):
+    assert validate(dict(BASE, move="M5", **{key: "x"}), CAT["moves"]["M5"])[2] == [f"bad_key:{key}"]
+
+
+def test_bad_field_from():
+    assert validate(dict(BASE, move="M5", **{"from": "t4-1"}), CAT["moves"]["M5"])[2] == ["bad_field:from"]
+
+
+def test_bad_move():
+    assert validate(dict(BASE, move="M11"), "x")[2] == ["bad_move"]
+
+
+def test_leak_text_differs():
+    assert validate(dict(BASE, move="M5"), CAT["moves"]["M5"] + " see Task 3")[2] == ["leak"]
+
+
+def test_leak_suffix_on_reading_move():
+    assert validate(dict(BASE, move="M5"), CAT["moves"]["M5"] + CAT["observable_suffix"])[2] == ["leak"]
+
+
+def test_not_json():
+    assert validate("{not json", "x")[2] == ["not_json"]
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_settings_and_cmd.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_settings_and_cmd.py
new file mode 100644
index 000000000..c202237b3
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_settings_and_cmd.py
@@ -0,0 +1,27 @@
+"""T-10 (settings part): settings-gen.sh output."""
+
+import json
+
+from conftest import TOOLS, run
+
+
+def test_settings_json(tmp_path):
+    board = str(tmp_path / "runs" / "el2-c1-r0" / "P" / "board")
+    args = [board, "el2-c1-r0/P", "t4-1", "reader", "1763062000000", "1763062143800", "1763062109600", "2", "8", "12",
+            "M3,M5,M6,M9,M8,M10", "P", ""]
+    r = run(["bash", str(TOOLS / "settings-gen.sh"), *args])
+    assert r.returncode == 0, r.stderr
+    d = json.loads(r.stdout)
+    h = d["hooks"]["PostToolUse"]
+    assert len(h) == 1 and h[0]["matcher"] == "*" and len(h[0]["hooks"]) == 1
+    cmd = h[0]["hooks"][0]
+    assert cmd["type"] == "command" and cmd["timeout"] == 5
+    assert "$" not in r.stdout
+    for v in (board, "'t4-1'", "'1763062000000'", "'1763062143800'", str(TOOLS / "radar-hook.sh")):
+        assert v in cmd["command"]
+    assert cmd["command"].endswith(" ''")
+
+
+def test_settings_refuses_unsafe_value(tmp_path):
+    args = ["/b", "r", "t4-1", "reader", "0", "1", "1", "2", "8", "12", "M3", "P$(id)", ""]
+    assert run(["bash", str(TOOLS / "settings-gen.sh"), *args]).returncode == 2
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py
new file mode 100644
index 000000000..cdac35697
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py
@@ -0,0 +1,35 @@
+"""Fault-injection tests F-1..F-14 (DESIGN.md section 6.2)."""
+
+import json
+
+from conftest import ctx_text
+
+
+# F-6: snapshot failure -> snapshot_missing 1, zero deliveries (same mechanism as T-7)
+def test_f6_snapshot_failure(board, tmp_path):
+    outs = [board.call("t4-1", "reader", transcript=tmp_path / "nope.jsonl") for _ in range(13)]
+    assert all(o == "" for o in outs)
+    assert len(board.events("t4-1", "snapshot_missing")) == 1 and board.events("t4-1", "inject") == []
+
+
+# F-7: a garbage line in tele/ does not change the hook's output
+def test_f7_corrupt_board_line(board, tmp_path):
+    from conftest import Board
+    clean = Board(tmp_path / "clean")
+    board.tele("t2b-1", "\x00garbage{")
+    a = [board.call("t2b-1", "searcher") for _ in range(10)]
+    b = [clean.call("t2b-1", "searcher") for _ in range(10)]
+    assert [bool(x) for x in a] == [bool(x) for x in b] and ctx_text(a[9]) == ctx_text(b[9])
+
+
+# F-14: env -i PATH=/usr/bin:/bin gives the same decisions and outputs
+def test_f14_environment_cleared(board, tmp_path):
+    from conftest import Board
+    other = Board(tmp_path / "envi")
+    env = {"PATH": "/usr/bin:/bin"}
+    a = [board.call("t2b-1", "searcher") for _ in range(11)]
+    b = [other.call("t2b-1", "searcher", env=env) for _ in range(11)]
+    assert a == b
+    strip = lambda evs: [{k: v for k, v in e.items() if k not in ("ms",)} for e in evs if e["ev"] != "t"]  # noqa: E731
+    assert strip(board.metrics("t2b-1")) == strip(other.metrics("t2b-1"))
+    assert json.loads(a[5]) and json.loads(a[9])

Codegraph context
index_state=fresh checked_at=2026-11-13T20:27:49Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b: the changed files are shell, jq, JSON and Python under .dev (eval harness, no product symbols have dependents outside the touched set); dependents checked on the Grep/Read floor: none outside the touched set.
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq
index 000000000..866ee22ab 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq
@@ -1,9 +1,9 @@
 # radar-classify.jq: the deterministic classifier (R-31). One tele record in, {"n":..,"sig":[..]} out.
 # Usage: jq -c --slurpfile ix index/<pkg>.json --arg srcpath SB/cand/<pkg>/source.md -f radar-classify.jq
 # Signatures: M1 M2 M4 M7 SRC_OPENED UNNAMED_TEST (never M3 M5 M6 M8 M9 M10). DESIGN.md section 2.3.
-# Input lines may be raw text (jq -R): unparsable lines are skipped.
+# Input lines may be raw text (jq -R): unparsable lines and lines that are not JSON objects are skipped.
 
-def rec: if type == "string" then (fromjson? // empty) else . end;
+def rec: (if type == "string" then (fromjson? // empty) else . end) | select(type == "object");
 ($ix[0]) as $ix
 | ($srcpath | sub("/cand/(?<p>[^/]+)/source\\.md$"; "/\(.p)/repo")) as $repo
 | ($srcpath | capture("/cand/(?<p>[^/]+)/source\\.md$").p // "") as $pkg
@@ -26,7 +26,7 @@ def rec: if type == "string" then (fromjson? // empty) else . end;
   | . as $r
   | (if ($r.sub // false) then []
      else
-       ($r.tool) as $tool | ($r.input // {}) as $in
+       ($r.tool) as $tool | ($r.input | if type == "object" then . else {} end) as $in
        | (if $tool == "Bash" then ($in.command // "" | tostring) else "" end) as $cmd
        | ($cmd | segs) as $segs
        | (if $tool == "Grep" then {pat: ($in.pattern // "" | tostring), gpath: (if $in.path then ($in.path | norm) else null end), mode: ($in.output_mode // null)} else null end) as $g
@@ -35,7 +35,9 @@ def rec: if type == "string" then (fromjson? // empty) else . end;
            (if ($segs | any(recursive and (pathargs | any(under_tests)))) and ($cmd | has_entry) then "M1" else empty end),
            (if $g and ($g.gpath // "." | under_tests) and ($g.pat | has_entry) then "M1" else empty end),
            # M2: listing or counting across a directory
-           (if $tool == "Bash" and ($cmd | test("\\bgrep\\s+(\\S+\\s+)*-[A-Za-z]*[lcL][A-Za-z]*(\\s|$)|\\bgrep\\s+-[lcL]\\b|\\bfind\\s|\\|\\s*wc\\s+-l")) then "M2" else empty end),
+           # (the -l/-c/-L test looks only at the option tokens of each grep segment, never at later commands)
+           (if $tool == "Bash" and (($segs | any(.tool != "rg" and (.rest | toks | any(test("^-[A-Za-z]*[lcL][A-Za-z]*$")))))
+                                    or ($cmd | test("\\bfind\\s|\\|\\s*wc\\s+-l"))) then "M2" else empty end),
            (if $g and ($g.mode == "files_with_matches" or $g.mode == "count") then "M2" else empty end),
            # M4: grep whose pattern equals a quoted criterion pattern
            (if ($segs | any(.tool != "rg" and (pattern as $p | $ix.criterion_greps | index($p) != null))) then "M4" else empty end),
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-hook.sh
index 000000000..8c1465e74 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-hook.sh
@@ -67,7 +67,7 @@ main() {
   ix=$BOARD/ctx/index.json; panel=$BOARD/ctx/panel.json
   local srcpath; srcpath=$(jq -r .srcpath "$panel")
   classify() { jq -R -c --slurpfile ix "$ix" --arg srcpath "$srcpath" -f "$TOOLS/radar-classify.jq" "$@" | jq -r '.sig[]'; }
-  local injected; injected=$(jq -R -r 'fromjson? // empty | select(.ev == "inject") | .move // "SRC"' "$MET" 2>/dev/null || true)
+  local injected; injected=$(jq -R -r 'fromjson? // empty | select(type == "object" and .ev == "inject") | .move // "SRC"' "$MET" 2>/dev/null || true)
   item=""
   local own=""; [ "$n" = "$CP1" ] && own=$(classify "$BOARD/tele/$RID.jsonl")
   if [ "$n" = "$CP1" ] && ! grep -qx SRC_OPENED <<< "$own"; then
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
index 000000000..45ddedcd9 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
@@ -109,6 +109,19 @@ class Board:
         p = self.dir / "metrics" / f"{rid}.jsonl"
         return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
 
+    def metrics_safe(self, rid):
+        """Metrics lines that are JSON objects (a test may plant junk lines)."""
+        p = self.dir / "metrics" / f"{rid}.jsonl"
+        out = []
+        for x in p.read_text().splitlines() if p.exists() else []:
+            try:
+                v = json.loads(x)
+            except ValueError:
+                continue
+            if isinstance(v, dict):
+                out.append(v)
+        return out
+
     def events(self, rid, ev):
         return [m for m in self.metrics(rid) if m.get("ev") == ev]
 
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_classify.py
index 000000000..e0e5fef4c 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_classify.py
@@ -46,6 +46,9 @@ NEG = [
     ("M1", bash("grep -rn unrelated_word tests/")),
     ("UNNAMED_TEST", tool("Read", file_path=f"{REPO}/tests/app/test_core.py")),
     ("M4", bash('grep -n "HOW-WE-WOR" docs/guide.md')),
+    ("M2", bash("grep -rn x src/ | head -c 500")),
+    ("M2", bash("grep -n x f; ls -la")),
+    ("M2", bash("grep -n x f && sort -c f")),
 ]
 
 
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_errors.py
index 000000000..48110541b 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_hook_errors.py
@@ -11,6 +11,19 @@ def test_corrupt_peer_line(board):
     assert ctx_text(outs[5])
 
 
+def test_non_object_json_lines_skipped(board):
+    # lines that parse but are not objects, last in the peer file and in the metrics file
+    for junk in ("[1]", "42", '"x"', '{"n":1,"tool":"Bash","input":"not an object"}'):
+        board.tele("t4-1", junk)
+    outs = [board.call("t2b-1", "searcher") for _ in range(10)]
+    with (board.dir / "metrics" / "t2b-1.jsonl").open("a") as f:
+        f.write("[1]\n")
+    board.call("t2b-1", "searcher")
+    assert ctx_text(outs[5]) and ctx_text(outs[9])
+    assert not [m for m in board.metrics_safe("t2b-1") if m.get("ev") == "hook_error"]
+    assert len([m for m in board.metrics_safe("t2b-1") if m.get("ev") == "inject"]) == 2
+
+
 def test_unwritable_msgs(board):
     (board.dir / "msgs").mkdir()
     os.chmod(board.dir / "msgs", 0o500)

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T3.AC1 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq:6 anchor="the four tools implement the behaviour of DESIGN.md sections 2.2, 2.3, 2.4 and 2.5" chk=y,n,n,n family=corrupt-line-breaks-hook fix=make `rec` drop non-objects, e.g. `def rec: (if type == "string" then (fromjson? // empty) else . end) | select(type == "object");`, and add a T-8/F-7 case with a JSON-parsable non-object peer line (`[1]`) as the last tele line first=A1 origin=new covers="2.4 step 4: readers skip unparsable lines with `fromjson? // empty`, so a torn or corrupt line never breaks a hook, R-22": `rec` only skips lines that do not parse. A corrupt line that parses as a non-object (`[1]`, `42`, `"x"`) reaches `$r.sub` at radar-classify.jq:27, and jq exits 5 when that line is the last input. In the hook, `covered=$(cat "$BOARD"/tele/*.jsonl | classify | sort -u)` (radar-hook.sh:77) runs under `set -e -o pipefail`, so the searcher's checkpoint becomes `hook_error` and nothing is injected. Reproduced: a peer tele file ending in `[1]` cut the searcher from 2 injections (calls 6 and 10) to 1, with `hook_error` 1. The same applies to the own-tele classify at :72. The current F-7 and T-8 garbage lines (`\x00garbage{` and `{"n":1,"tool":"Bash","inp`) do not parse, so they never reach this path.
F1.2 sev=blocking trigger=B1 ac=T3.AC1 at=.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq:38 anchor="the four tools implement the behaviour of DESIGN.md sections 2.2, 2.3, 2.4 and 2.5" chk=y,n,n,n family=classifier-m2-overmatch fix=test the l/c/L flag cluster only on option tokens of the grep segment itself (reuse `segs` with the token split, as M1 and M7 do), not with a regex over the whole command after the word grep; add T-3 negatives `grep -rn x src/ | head -c 500` and `grep -n x f; ls -la` first=A1 origin=new covers="DESIGN.md 2.3 M2: Bash `cmd` contains `grep -l`, `grep -c`, `grep -L`, combined short flags containing `l` or `c` after `grep -`, `find `, or a pipe into `wc -l`": The M2 regex `\bgrep\s+(\S+\s+)*-[A-Za-z]*[lcL][A-Za-z]*(\s|$)` lets `(\S+\s+)*` run over `|`, `;` and `&&`. Any later token of another command that contains l, c or L therefore fires M2 (`| head -c 500`, `; ls -la`, `&& sort -c`); all three were reproduced. In the hook this marks M2 as covered by the panel when no grep listing or count ran, so the searcher's M2 is skipped silently (2.5 (b)). The post-hoc `move_executed` and `moves_covered` counters built on the same classifier are inflated too.

Saved-probe re-check hit locations (may be empty): .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-hook.sh:70:  local injected; injected=$(jq -R -r 'fromjson? // empty | select(type == "object" and .ev == "inject") | .move // "SRC"' "$MET" 2>/dev/null || true)
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq:6:def rec: (if type == "string" then (fromjson? // empty) else . end) | select(type == "object");
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq:18:  def recursive: .tool == "rg" or (.rest | test("(^|\\s)(-[A-Za-z]*[rR][A-Za-z]*|--recursive)(\\s|$)"));
39:           (if $tool == "Bash" and (($segs | any(.tool != "rg" and (.rest | toks | any(test("^-[A-Za-z]*[lcL][A-Za-z]*$")))))


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
