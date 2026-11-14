18e8eb6d54a0d71c1c5225866b836a06a0a4f681
## family corrupt-line-breaks-hook (from r1-1)
defect form: a tele line that parses as JSON but is not an object reaches field access in the classifier and makes jq exit non-zero
command: grep -n -e 'def rec' -e 'fromjson' .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-hook.sh
before:
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq:6:def rec: if type == "string" then (fromjson? // empty) else . end;
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq:18:  def recursive: .tool == "rg" or (.rest | test("(^|\\s)(-[A-Za-z]*[rR][A-Za-z]*|--recursive)(\\s|$)"));
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-hook.sh:70:  local injected; injected=$(jq -R -r 'fromjson? // empty | select(.ev == "inject") | .move // "SRC"' "$MET" 2>/dev/null || 
coupled sites: radar-classify.jq rec (single entry point used by the hook's own-tele and panel classify calls, radar-hook.sh:72 and :77); radar-hook.sh injected-moves read of metrics (fromjson? // empty | select(.ev == "inject") on objects only); tests test_hook_errors.py / test_faults.py F-7 need a non-object line case
## family classifier-m2-overmatch (from r1-1)
defect form: a regex over the whole command after the word grep lets later commands' flags (| head -c, ; ls -la) count as grep -l/-c
command: grep -n -e 'lcL' .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq
before:
38:           (if $tool == "Bash" and ($cmd | test("\\bgrep\\s+(\\S+\\s+)*-[A-Za-z]*[lcL][A-Za-z]*(\\s|$)|\\bgrep\\s+-[lcL]\\b|\\bfind\\s|\\|\\s*wc\\s+-l")) then "M2" else empty end),
coupled sites: radar-classify.jq M2 Bash rule only (M1/M4/M7 already use segs); tests test_classify.py NEG list
after (corrupt-line-breaks-hook):
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-hook.sh:70:  local injected; injected=$(jq -R -r 'fromjson? // empty | select(type == "object" and .ev == "inject") | .move // "SRC"' "
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq:6:def rec: (if type == "string" then (fromjson? // empty) else . end) | select(type == "object");
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/radar-classify.jq:18:  def recursive: .tool == "rg" or (.rest | test("(^|\\s)(-[A-Za-z]*[rR][A-Za-z]*|--recursive)(\\s|$)"));
after (classifier-m2-overmatch):
39:           (if $tool == "Bash" and (($segs | any(.tool != "rg" and (.rest | toks | any(test("^-[A-Za-z]*[lcL][A-Za-z]*$")))))
