3412774a33ebf802058ad53f42523c663de5742c
Review one task for spec compliance.

Task brief: ## Task 11: Complete the fake claude and test it

Depends on: Task 10

Follow `RL/IMPLEMENTATION.md` step 5 (first sentence) and `RL/DESIGN.md` 3.4. Extend `RL/tests/fakes/claude` with every scenario: `ok`, `problem` (one PROBLEM row with exact quotes from the candidate and a linked finding), `none_found`, `ledger_missing`, `ledger_after_findings`, `over_budget`, `recipe_missing`, `long_anchor`, `bad_block`, `api_error`, `wrong_model`, `sleep` (`FAKE_SLEEP_S`), `exit127` and `repair` (a second call whose brief starts with the repair sentence of `RL/DESIGN.md` 7.6 returns the first message with a ledger added). `FAKE_SCENARIO_BY_MODEL` may set a scenario per requested model. Each call appends `<epoch seconds> TAB <scenario> TAB <requested model> TAB <review or repair>` to `FAKE_CALL_LOG`. Write `RL/tests/test_fake_claude_rl.py::test_scenarios_and_call_log` (each scenario prints the JSON array of its description, one log line per call, the suite fails if the first `claude` on `PATH` is not the fake).

Acceptance criteria (ids added by the orchestrator, in source order):
T11.AC1: `$T $RL/tests/test_fake_claude_rl.py -q` exits 0.
T11.AC2: No scenario starts a model or makes a network call.
T11.AC3: The `repair` scenario is selected by the brief starting with the repair sentence and returns a message whose findings block equals the first message's.

Global constraints: ## Constraints

Path names used by every task (all repo-relative to the checkout root `REPO`, which is `git rev-parse --show-toplevel`):

- `RL` is `.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger`. It holds `DESIGN.md`, `TESTING.md`, `IMPLEMENTATION.md` and `SHARED-MANIFEST-DESIGN-TIME.tsv`, which are the specification and are never edited by the build.
- `SW` is `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet`, the sibling build (Redesign 1). It is read only: no task writes, edits, moves or deletes anything under it, and no task runs a script or a test from inside it.
- `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md` (sections 3.0, 3.2, 5 and 6 are the requirements source; the design documents already map them). `EVAL` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only).
- Design ids: `K1` to `K9` (constraints), `DR-1` to `DR-16` (decisions) and `REQ-nn` (requirements) are those of `RL/DESIGN.md` sections 1.2 and 1.3 and of `RL/TESTING.md` section 3.

Scope rules that hold for every task:

- Create or edit files only under `RL`, plus scratch under `/tmp` (sandboxes under `/tmp/evalsb-recipe`, scratch under `/tmp/rl-*`). Nothing under `src/`, `tests/`, `.claude/`, any existing folder under `.dev/tasks/`, `SW`, `EVAL`, `.dev/eval-workspaces/tasklist-review-panel/20261113-collab` or any other folder is changed.
- No task runs `git commit` or `git push`, and no task runs `git add` for a path under `RL`. The freeze tag (K5) is only printed, never created.
- No task opens, reads, greps the content of or copies any `ground-truth*.json`, score file or judge output of a study package, and no recipe, card, brief, fixture, regex or example uses a study answer. Fixtures are invented. Tests that need ground truth use the synthetic `RL/fixtures/gt/` files only. The tests marked `freeze` (they read the real ground truth or need a second author's records) are never run by this build.
- Python runs only through uv. No `python -m`, no bare `pip`. No code folder is named `lib/` (K7).
- No reviewer or judge session is started and no network call is made. Tests use the fake `claude` at `RL/tests/fakes/claude`. If a task ever needed a model it would use `claude-sonnet-5-5` or `claude-haiku-5-5`; Opus is only the blind judge script's model; never Qwen or glm.
- Files under `RL/scaffold/`, `RL/cards/`, `RL/briefs/`, `RL/bin/common.sh`, `RL/bin/build-sandbox.sh` and the copied tests are copies of sibling files and are never edited after the copy (DESIGN 3.1). A copied test that fails is reported, not edited.
- Shell variables used in task commands:

```
REPO=$(git rev-parse --show-toplevel)
RL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
MR=$REPO/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
PYRUN="uv run --frozen --project $REPO python"
export PYTHONDONTWRITEBYTECODE=1 NOFALLBACK=1 SUPERCLAUDE_CODEGRAPH_AUTOINIT=0
```


Start sha: 3412774a33ebf802058ad53f42523c663de5742c
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/fakes/claude b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/fakes/claude
index d06c2c3a7..199289f92 100755
--- a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/fakes/claude
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/fakes/claude
@@ -1,11 +1,33 @@
 #!/usr/bin/env bash
-# Stand-in for `claude -p --output-format json` (TESTING F-FAKE-RL). No model is started.
-# Reads the brief on stdin, picks a scenario from FAKE_SCENARIO (default ok), prints the JSON array of a
-# real run (system init, one assistant message, result) and appends one line per call to FAKE_CALL_LOG:
+# Stand-in for `claude -p --output-format json` (TESTING F-FAKE-RL, DESIGN 3.4). No model is started, no network is used.
+# Reads the brief on stdin, picks a scenario from FAKE_SCENARIO (default ok), prints the JSON array of a real run
+# (system init, assistant, user tool results where the scenario has a tool call, final assistant, result) and appends
+# one line per call to FAKE_CALL_LOG:
 #   <epoch seconds> TAB <scenario> TAB <requested model> TAB <kind: review or repair>
-# Scenario now: ok. The others of DESIGN 3.4 are added in task 11.
-# Ledger rows: for every recipe heading `R-C<n>.` of the brief, rows C<n>.1 to C<n>.<budget>, all OK; the budget
-# is the N of the recipe's sentence `Write at most N rows.` (4 when the recipe has none). No recipe, no ledger.
+# FAKE_SCENARIO_BY_MODEL: space-separated model=scenario pairs; a call for that model uses that scenario.
+# A brief that starts with the repair sentence of DESIGN 7.6 is the `repair` kind: the scenario is `repair` for it,
+# whatever the variables say, and it must not be set by hand.
+# Scenarios (rows are written for every recipe heading `R-C<n>.` of the brief; the budget is the N of the recipe's
+# sentence `Write at most N rows.`, 4 when it has none; no recipe, no ledger):
+#   ok                    rows C<n>.1 .. C<n>.<budget> for every recipe, all OK
+#   problem               as ok, but row C<first>.1 is PROBLEM with two exact candidate quotes and a Bash grep call,
+#                         and a blocking finding (CB-3 sentence in its claim) whose anchor holds the row's quote_plan
+#   none_found            one row C<n>.1 per recipe: OK, empty quote_plan, ran "NONE FOUND"; one grep with no output
+#   ledger_missing        findings block, no ledger
+#   ledger_after_findings the ledger block comes after the findings block
+#   over_budget           one row more than the budget for every recipe
+#   recipe_missing        the last recipe has no row (an empty ledger when there is only one recipe)
+#   long_anchor           the finding's anchor is 250 characters of the candidate (the parser limit is 200)
+#   bad_block             a findings line that is not JSON
+#   api_error             an error result, observed model <synthetic>
+#   wrong_model           another model than the requested one is observed
+#   sleep                 waits FAKE_SLEEP_S seconds (default 5; ends on TERM with exit 143), then answers as ok
+#   exit127               prints `command not found` on stderr, exit 127, no output
+#   repair                the message between the lines BEGIN and END with a ledger added directly above its
+#                         `## Findings block` (an old ledger section is removed); rows C<n>.1 for the classes of
+#                         the message's line `Recipes run: ...`; the findings block is not touched
+# The review message names its recipes in that line so the repair call, which sees only the message, can find them.
+# Quotes come from the candidate: the path after `Review the candidate` in the brief, else ./candidate.md.
 set -u
 SCEN=${FAKE_SCENARIO:-ok}
 MODEL=claude-sonnet-5-5
@@ -13,48 +35,157 @@ while [ $# -gt 0 ]; do
   [ "$1" = "--model" ] && [ $# -ge 2 ] && MODEL=$2
   shift
 done
+for kv in ${FAKE_SCENARIO_BY_MODEL:-}; do
+  [ "${kv%%=*}" = "$MODEL" ] && SCEN=${kv#*=}
+done
 BRIEF=$(cat)
 
+KIND=review
+case "$BRIEF" in "Your final message was kept as your review"*) KIND=repair; SCEN=repair ;; esac
 case "$SCEN" in
-  ok) ;;
+  ok | problem | none_found | ledger_missing | ledger_after_findings | over_budget | recipe_missing) ;;
+  long_anchor | bad_block | api_error | wrong_model | sleep | exit127) ;;
+  repair) [ "$KIND" = repair ] || { echo "fake claude: the repair scenario is chosen by a repair brief" >&2; exit 2; } ;;
   *) echo "fake claude: unknown FAKE_SCENARIO=$SCEN" >&2; exit 2 ;;
 esac
-
-KIND=review
-case "$BRIEF" in "Your final message was kept as your review"*) KIND=repair ;; esac
 [ -z "${FAKE_CALL_LOG:-}" ] || printf '%s\t%s\t%s\t%s\n' "$(date +%s.%3N)" "$SCEN" "$MODEL" "$KIND" >>"$FAKE_CALL_LOG"
 
-# One "<class> <budget>" line per recipe, in brief order: the text between a heading and the next heading or blank line.
-RECIPES=$(printf '%s\n' "$BRIEF" | awk '
-  function flush() { if (cls != "") print cls, (n == "" ? 4 : n); cls = ""; n = "" }
-  /^R-C[0-9]+\. / { flush(); cls = $1; sub(/^R-/, "", cls); sub(/\.$/, "", cls) }
-  cls != "" && match($0, /Write at most [0-9]+ rows\./) {
-    s = substr($0, RSTART, RLENGTH); gsub(/[^0-9]/, "", s); n = s
-  }
-  /^$/ { flush() }
-  END { flush() }')
-
-LEDGER=""
-while read -r cls budget; do
-  [ -n "${cls:-}" ] || continue
-  for k in $(seq 1 "$budget"); do
-    LEDGER+=$(jq -nc --arg i "$cls.$k" '{item:$i,verdict:"OK",quote_plan:"",quote_other:"",problem:"",ran:"compared both scopes"}')$'\n'
+if [ "$SCEN" = exit127 ]; then
+  echo "claude: command not found" >&2
+  exit 127
+fi
+if [ "$SCEN" = sleep ]; then
+  sleep "${FAKE_SLEEP_S:-5}" &
+  trap 'kill $! 2>/dev/null; exit 143' TERM INT
+  wait $!
+fi
+
+BT='```'
+OBS=$MODEL
+ISERR=false
+TOOL_CMD=""
+TOOL_OUT=""
+
+if [ "$SCEN" = repair ]; then
+  MSG=$(printf '%s\n' "$BRIEF" | awk '
+    { line[NR] = $0 }
+    $0 == "BEGIN" && !b { b = NR }
+    $0 == "END" { e = NR }
+    END { for (i = b + 1; i < e; i++) print line[i] }')
+  LEDGER=""
+  for cls in $(printf '%s\n' "$MSG" | sed -n 's/^.*Recipes run: //p' | grep -oE 'C[0-9]+'); do
+    LEDGER+=$(jq -nc --arg i "$cls.1" '{item:$i,verdict:"OK",quote_plan:"",quote_other:"",problem:"",ran:"compared both scopes"}')$'\n'
   done
-done <<<"$RECIPES"
+  SECTION="## Ledger"$'\n\n'"${BT}ledger-v1"$'\n'"${LEDGER}${BT}"$'\n\n'
+  # drop an old ledger section (heading, fenced block), then add the new one above the findings heading
+  REPORT=$(printf '%s\n' "$MSG" | SECTION=$SECTION awk '
+    skip == 1 && /^```ledger-v1/ { skip = 2; next }
+    skip == 2 { if ($0 ~ /^```/) skip = 3; next }
+    skip == 3 && /^$/ { skip = 0; next }
+    skip == 1 && /^$/ { next }
+    /^## Ledger/ { skip = 1; next }
+    /^## Findings block/ { printf "%s", ENVIRON["SECTION"] }
+    { print }')
+else
+  # recipes of the brief, one "<class> <budget>" line each, in brief order: the text between a heading and the next
+  # heading or blank line
+  RECIPES=$(printf '%s\n' "$BRIEF" | awk '
+    function flush() { if (cls != "") print cls, (n == "" ? 4 : n); cls = ""; n = "" }
+    /^R-C[0-9]+\. / { flush(); cls = $1; sub(/^R-/, "", cls); sub(/\.$/, "", cls) }
+    cls != "" && match($0, /Write at most [0-9]+ rows\./) {
+      s = substr($0, RSTART, RLENGTH); gsub(/[^0-9]/, "", s); n = s
+    }
+    /^$/ { flush() }
+    END { flush() }')
+  [ "$SCEN" != recipe_missing ] || RECIPES=$(printf '%s\n' "$RECIPES" | sed '$d')
 
-FINDING=$(jq -nc '{id:"F1",severity:"MINOR",blocking:false,category:"other",anchor:"the stated text of the first acceptance criterion",refs:[],claim:"The wording leaves one reading open."}')
+  CAND=$(printf '%s\n' "$BRIEF" | sed -nE 's/^.*Review the candidate ([^ ]+) .*$/\1/p' | head -n1)
+  [ -f "$CAND" ] || CAND=candidate.md
+  Q1=""
+  Q2=""
+  ANCHOR="the stated text of the first acceptance criterion"
+  if [ -f "$CAND" ]; then
+    # two different candidate lines of 12 to 200 characters, bullets first, without the bullet mark
+    QS=$({ grep -E '^[[:space:]]*- ' "$CAND"; cat "$CAND"; } | sed -E 's/^[[:space:]]*(- )?//' |
+      awk 'length($0) >= 12 && length($0) <= 200 && !seen[$0]++')
+    Q1=$(printf '%s\n' "$QS" | sed -n 1p)
+    Q2=$(printf '%s\n' "$QS" | sed -n 2p)
+    ANCHOR=$Q1
+    [ "$SCEN" != long_anchor ] || ANCHOR=$(tr -s '[:space:]' ' ' <"$CAND" | cut -c1-250)
+  elif [ "$SCEN" = problem ] || [ "$SCEN" = long_anchor ]; then
+    echo "fake claude: scenario $SCEN needs the candidate named in the brief or ./candidate.md" >&2
+    exit 2
+  fi
 
-BT='```'
-REPORT="review: 1 of 3"$'\n\n'"Covered: the candidate and the source."$'\n\n'
-if [ -n "$LEDGER" ]; then
-  REPORT+="## Ledger"$'\n\n'"${BT}ledger-v1"$'\n'"${LEDGER}${BT}"$'\n\n'
+  LEDGER=""
+  FIRST=1
+  while read -r cls budget; do
+    [ -n "${cls:-}" ] || continue
+    [ "$SCEN" != over_budget ] || budget=$((budget + 1))
+    [ "$SCEN" != none_found ] || budget=1
+    for k in $(seq 1 "$budget"); do
+      ROW=$(jq -nc --arg i "$cls.$k" '{item:$i,verdict:"OK",quote_plan:"",quote_other:"",problem:"",ran:"compared both scopes"}')
+      if [ "$SCEN" = problem ] && [ "$FIRST" = 1 ]; then
+        ROW=$(jq -nc --arg i "$cls.$k" --arg a "$Q1" --arg b "$Q2" '{item:$i,verdict:"PROBLEM",quote_plan:$a,quote_other:$b,problem:"The two stated texts do not agree.",ran:"read both statements"}')
+      elif [ "$SCEN" = none_found ]; then
+        ROW=$(jq -nc --arg i "$cls.$k" '{item:$i,verdict:"OK",quote_plan:"",quote_other:"",problem:"",ran:"NONE FOUND"}')
+      fi
+      FIRST=0
+      LEDGER+=$ROW$'\n'
+    done
+  done <<<"$RECIPES"
+
+  SEVERITY=MINOR
+  BLOCKING=false
+  CLAIM="The wording leaves one reading open."
+  VERDICT=PASS
+  if [ "$SCEN" = problem ]; then
+    SEVERITY=MAJOR
+    BLOCKING=true
+    CLAIM="An implementer who follows the stated text as written builds the first reading, and that is wrong because the second text states the other."
+    VERDICT=FAIL
+    TOOL_CMD="grep -n -F -m1 -- '$Q1' $CAND"
+    TOOL_OUT=$(grep -n -F -m1 -- "$Q1" "$CAND")
+  elif [ "$SCEN" = none_found ] && [ -f "$CAND" ]; then
+    TOOL_CMD="grep -n -F -m1 -- 'no-such-text-zq' $CAND"
+  fi
+  FINDING=$(jq -nc --arg a "$ANCHOR" --arg s "$SEVERITY" --argjson b "$BLOCKING" --arg c "$CLAIM" \
+    '{id:"F1",severity:$s,blocking:$b,category:"other",anchor:$a,refs:[],claim:$c}')
+  [ "$SCEN" != bad_block ] || FINDING="{not json"
+
+  RUN=""
+  [ -z "$RECIPES" ] || RUN=" Recipes run: $(printf '%s\n' "$RECIPES" | awk '{print $1}' | paste -sd' ' -)."
+  REPORT="review: 1 of 3"$'\n\n'"Covered: the candidate and the source.${RUN}"$'\n\n'
+  LEDGER_SECTION="## Ledger"$'\n\n'"${BT}ledger-v1"$'\n'"${LEDGER}${BT}"$'\n\n'
+  FINDINGS_SECTION="## Findings block"$'\n\n'"${BT}findings-v1"$'\n'"${FINDING}"$'\n'"${BT}"$'\n\n'
+  case "$SCEN" in
+    ledger_missing) REPORT+="${FINDINGS_SECTION}verdict: ${VERDICT}" ;;
+    ledger_after_findings) REPORT+="${FINDINGS_SECTION}${LEDGER_SECTION}verdict: ${VERDICT}" ;;
+    *) if [ -n "$LEDGER" ] || [ "$SCEN" = recipe_missing ]; then REPORT+=$LEDGER_SECTION; fi
+       REPORT+="${FINDINGS_SECTION}verdict: ${VERDICT}" ;;
+  esac
+
+  if [ "$SCEN" = wrong_model ]; then
+    OBS=claude-haiku-5-5
+    [ "$MODEL" != claude-haiku-5-5 ] || OBS=gpt-6-luna
+  fi
+  if [ "$SCEN" = api_error ]; then
+    OBS="<synthetic>"
+    ISERR=true
+    REPORT="API Error: 529 overloaded_error"
+  fi
 fi
-REPORT+="## Findings block"$'\n\n'"${BT}findings-v1"$'\n'"${FINDING}"$'\n'"${BT}"$'\n\n'"verdict: PASS"
 
-jq -nc --arg m "$MODEL" --arg r "$REPORT" '
+jq -nc --arg m "$MODEL" --arg o "$OBS" --arg r "$REPORT" --argjson e "$ISERR" --arg tc "$TOOL_CMD" --arg to "$TOOL_OUT" '
   ($r | length / 4 | floor) as $n
-  | [ {type:"system", subtype:"init", session_id:"fake-session", model:$m},
-      {type:"assistant", parent_tool_use_id:null, session_id:"fake-session",
-       message:{model:$m, content:[{type:"text", text:$r}]}},
-      {type:"result", subtype:"success", is_error:false, result:$r, session_id:"fake-session",
-       usage:{output_tokens:$n}, modelUsage:{($m):{outputTokens:$n}}} ]'
+  | [ {type:"system", subtype:"init", session_id:"fake-session", model:$m} ]
+    + (if $tc == "" then [] else
+        [ {type:"assistant", parent_tool_use_id:null, session_id:"fake-session",
+           message:{model:$o, content:[{type:"tool_use", id:"toolu_01", name:"Bash", input:{command:$tc}}]}},
+          {type:"user", parent_tool_use_id:null, session_id:"fake-session",
+           message:{role:"user", content:[{type:"tool_result", tool_use_id:"toolu_01", content:$to}]}} ] end)
+    + [ {type:"assistant", parent_tool_use_id:null, session_id:"fake-session",
+         message:{model:$o, content:[{type:"text", text:$r}]}},
+        {type:"result", subtype:(if $e then "error_during_execution" else "success" end),
+         is_error:$e, result:$r, session_id:"fake-session",
+         usage:{output_tokens:$n}, modelUsage:{($o):{outputTokens:$n}}} ]'
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_fake_claude_rl.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_fake_claude_rl.py
new file mode 100644
index 000000000..ceca3c838
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_fake_claude_rl.py
@@ -0,0 +1,276 @@
+"""F-FAKE-RL (TESTING section 2): the fake claude is first on PATH and each of its scenarios behaves as the
+integration tests expect. The repair scenario is shown to give a message that rl.reask accepts. No model starts.
+"""
+
+import json
+import os
+import shutil
+import subprocess
+import time
+
+import pytest
+import rl_support as s
+from conftest import FAKES, assert_fake_first
+from helpers import SW
+
+from rl import ledger_api as api
+from rl import reask, render
+from scaffold import fnd
+
+EMBER = "muse-ember-1.0"
+LUNA = "gpt-6-luna"
+SCENARIOS = (
+    "ok",
+    "problem",
+    "none_found",
+    "ledger_missing",
+    "ledger_after_findings",
+    "over_budget",
+    "recipe_missing",
+    "long_anchor",
+    "bad_block",
+    "api_error",
+    "wrong_model",
+    "sleep",
+    "exit127",
+)
+ROLE = s.roles("primary")["S"]  # the ember role: C4 C5 C6 C8, four rows each
+CLASSES = ROLE["recipes"]
+PLAN = SW / "fixtures" / "plans" / "p_basic.md"
+
+
+@pytest.fixture
+def brief(tmp_path):
+    """The ember brief of the primary panel, naming a candidate copy under tmp_path."""
+    cand = tmp_path / "candidate.md"
+    cand.write_text(PLAN.read_text(encoding="utf-8"), encoding="utf-8")
+    doc = {"cand_sb": str(cand), "sha": s.SHA}
+    return render.brief(ROLE, doc, s.SOURCE)["text"], fnd.flat(cand.read_text())
+
+
+def call(roots, brief_text, scenario="ok", model=EMBER, **extra):
+    env = roots.with_env(FAKE_SCENARIO=scenario, **extra)
+    assert shutil.which("claude", path=env["PATH"]) == str(FAKES / "claude")
+    return subprocess.run(
+        ["claude", "-p", "--model", model, "--output-format", "json"],
+        input=brief_text,
+        capture_output=True,
+        text=True,
+        env=env,
+        timeout=30,
+        cwd=roots.root,
+    )
+
+
+def parts(r):
+    ev = json.loads(r.stdout)
+    return ev, ev[-1]
+
+
+def log(roots):
+    if not roots.call_log.exists():
+        return []
+    return [ln.split("\t") for ln in roots.call_log.read_text().splitlines()]
+
+
+def row_ids(report):
+    return [r["item"] for r in api.read(report)["rows"]]
+
+
+def expected_ids(extra=0):
+    return [f"{c}.{k}" for c in CLASSES for k in range(1, 4 + extra + 1)]
+
+
+def test_first_claude_on_path_is_the_fake(tmp_roots):
+    env = tmp_roots.with_env()
+    assert shutil.which("claude", path=env["PATH"]) == str(FAKES / "claude")
+    assert_fake_first(env)
+    env["PATH"] = env["PATH"].split(os.pathsep, 1)[
+        1
+    ]  # without the fakes folder first, the check fails
+    with pytest.raises(AssertionError):
+        assert_fake_first(env)
+
+
+def test_scenarios_and_call_log(tmp_roots, brief):
+    text, cand = brief
+    for i, scen in enumerate(SCENARIOS, start=1):
+        r = call(tmp_roots, text, scen, FAKE_SLEEP_S="0.2")
+        if scen == "exit127":
+            assert r.returncode == 127 and r.stdout == ""
+            assert "command not found" in r.stderr
+        else:
+            assert r.returncode == 0, (scen, r.stderr)
+            events, res = parts(r)
+            types = [e["type"] for e in events]
+            tooled = ["system", "assistant", "user", "assistant", "result"]
+            assert types == (
+                tooled
+                if scen in ("problem", "none_found")
+                else ["system", "assistant", "result"]
+            ), scen
+            check_scenario(scen, events, res["result"], cand)
+        lines = log(tmp_roots)
+        assert len(lines) == i, scen
+        stamp, name, model, kind = lines[-1]
+        assert float(stamp) > 1e9 and (name, model, kind) == (scen, EMBER, "review")
+
+
+def check_scenario(scen, events, report, cand):
+    res = events[-1]
+    obs = events[1]["message"]["model"]
+    assert events[0]["subtype"] == "init" and events[0]["model"] == EMBER
+    if scen == "api_error":
+        assert obs == "<synthetic>" and res["is_error"]
+        assert report.startswith("API Error") and list(res["modelUsage"]) == [obs]
+        return
+    assert obs == (EMBER if scen != "wrong_model" else "claude-haiku-5-5")
+    assert not res["is_error"] and list(res["modelUsage"]) == [obs]
+    ledger, block = api.read(report), fnd.parse_block(report)
+    if scen in ("ok", "sleep"):
+        assert row_ids(report) == expected_ids() and not ledger["ledger_missing"]
+        assert [r["verdict"] for r in ledger["rows"]] == ["OK"] * 16
+        assert block["ok"] and len(block["findings"]) == 1
+        assert fnd.flat(block["findings"][0]["anchor"]) in cand
+        assert report.index("## Ledger") < report.index("## Findings block")
+        assert report.startswith("review: 1 of 3\n")
+    elif scen == "problem":
+        problems = [r for r in ledger["rows"] if r["verdict"] == "PROBLEM"]
+        assert [p["item"] for p in problems] == ["C4.1"]
+        row = api.check(problems, {"candidate": cand})[0]
+        assert row["quote_plan_ok"] and row["quote_other_ok"] and row["supported"]
+        assert row["corpus"] == "candidate"
+        finding = block["findings"][0]
+        assert finding["blocking"] and fnd.flat(row["quote_plan"]) in fnd.flat(
+            finding["anchor"]
+        )
+        assert (
+            "An implementer who follows the stated text as written builds"
+            in finding["claim"]
+        )
+        use, result = (
+            events[1]["message"]["content"][0],
+            events[2]["message"]["content"][0],
+        )
+        assert use["name"] == "Bash" and result["tool_use_id"] == use["id"]
+        assert fnd.flat(row["quote_plan"]) in fnd.flat(result["content"])
+        linked = api.link_demote(report, api.check(ledger["rows"], {"candidate": cand}))
+        assert linked["links"] == {"F1": "C4.1"} and not any(linked["demoted"].values())
+    elif scen == "none_found":
+        assert row_ids(report) == [f"{c}.1" for c in CLASSES]
+        assert all(
+            r["ran"] == "NONE FOUND" and not r["quote_plan"] for r in ledger["rows"]
+        )
+        assert (
+            events[2]["message"]["content"][0]["content"] == ""
+        )  # a search with no hit
+    elif scen == "ledger_missing":
+        assert ledger["ledger_missing"] and block["ok"] and "ledger-v1" not in report
+    elif scen == "ledger_after_findings":
+        assert ledger["ledger_missing"] and ledger["reason"] == "ledger_after_findings"
+        assert block["ok"] and "```ledger-v1" in report
+    elif scen == "over_budget":
+        assert row_ids(report) == expected_ids(extra=1)
+    elif scen == "recipe_missing":
+        assert row_ids(report) == [i for i in expected_ids() if not i.startswith("C8.")]
+        assert block["ok"]
+    elif scen == "long_anchor":
+        anchor = block["findings"][0]["anchor"] if block["ok"] else None
+        assert anchor is None  # the parser refuses an anchor above 200 characters
+        long = [ln for ln in report.splitlines() if ln.startswith('{"id":"F1"')][0]
+        assert len(json.loads(long)["anchor"]) == 250
+        assert json.loads(long)["anchor"] in cand
+    elif scen == "bad_block":
+        assert not block["ok"] and "not valid JSON" in block["errors"][0]["msg"]
+        assert not ledger["ledger_missing"]
+    elif scen == "wrong_model":
+        assert obs != EMBER
+
+
+def test_unknown_scenario_and_hand_set_repair_are_refused(tmp_roots, brief):
+    text, _ = brief
+    r = call(tmp_roots, text, "nope")
+    assert r.returncode == 2 and "unknown FAKE_SCENARIO" in r.stderr
+    r = call(tmp_roots, text, "repair")
+    assert r.returncode == 2 and "repair brief" in r.stderr
+
+
+def test_scenario_by_model(tmp_roots, brief):
+    text, _ = brief
+    by_model = f"{EMBER}=ledger_missing {LUNA}=none_found"
+    for model in (EMBER, LUNA, "claude-haiku-5-5"):
+        r = call(tmp_roots, text, "ok", model, FAKE_SCENARIO_BY_MODEL=by_model)
+        assert r.returncode == 0
+    assert [(m, n) for _, n, m, _ in log(tmp_roots)] == [
+        (EMBER, "ledger_missing"),
+        (LUNA, "none_found"),
+        ("claude-haiku-5-5", "ok"),
+    ]
+
+
+def test_sleep_waits_and_dies_on_term(tmp_roots, brief):
+    text, _ = brief
+    t = time.monotonic()
+    assert call(tmp_roots, text, "sleep", FAKE_SLEEP_S="0.5").returncode == 0
+    assert time.monotonic() - t >= 0.5
+    p = subprocess.Popen(
+        ["claude", "-p"],
+        stdin=subprocess.PIPE,
+        stdout=subprocess.PIPE,
+        text=True,
+        env=tmp_roots.with_env(FAKE_SCENARIO="sleep", FAKE_SLEEP_S="30"),
+    )
+    p.stdin.write(text)
+    p.stdin.close()
+    time.sleep(0.5)
+    p.terminate()
+    assert p.wait(timeout=5) == 143
+
+
+# ---------------------------------------------------------------- repair
+
+
+def first_message(roots, text, scenario):
+    return parts(call(roots, text, scenario))[1]["result"]
+
+
+@pytest.mark.parametrize("scenario", ["ledger_missing", "ledger_after_findings"])
+def test_repair_keeps_the_findings_block_and_is_accepted(tmp_roots, brief, scenario):
+    text, _ = brief
+    original = first_message(tmp_roots, text, scenario)
+    assert api.read(original)["ledger_missing"]
+    # the variables still name the broken scenario: the brief alone selects the repair
+    r = call(tmp_roots, reask.repair_prompt(original), scenario)
+    assert r.returncode == 0
+    events, res = parts(r)
+    assert [e["type"] for e in events] == ["system", "assistant", "result"]
+    repaired = res["result"]
+    assert [x[1:] for x in log(tmp_roots)[-1:]] == [["repair", EMBER, "repair"]]
+    assert row_ids(repaired) == [f"{c}.1" for c in CLASSES]
+    assert repaired.count("## Ledger") == 1 and repaired.count("```ledger-v1") == 1
+    assert repaired.index("## Ledger") < repaired.index("## Findings block")
+    assert (
+        fnd.parse_block(repaired)["findings"] == fnd.parse_block(original)["findings"]
+    )
+    assert reask._findings_lines(repaired) == reask._findings_lines(original)
+    assert reask.accept(original, repaired) == (True, "accepted")
+
+
+def test_run_reask_calls_the_fake_and_accepts(tmp_roots, brief):
+    text, _ = brief
+    original = first_message(tmp_roots, text, "ledger_missing")
+    env = tmp_roots.with_env(FAKE_SCENARIO="ledger_missing")
+
+    def run(argv, stdin_text, cwd):
+        p = subprocess.run(
+            argv, input=stdin_text, capture_output=True, text=True, env=env, cwd=cwd
+        )
+        return p.returncode, p.stdout, p.stderr
+
+    rec = reask.run_reask(original, EMBER, tmp_roots.root, run=run)
+    assert rec["accepted"] and rec["reason"] == "accepted" and rec["model_ok"]
+    assert not api.read(rec["message"])["ledger_missing"]
+    assert [x[1:] for x in log(tmp_roots)] == [
+        ["ledger_missing", EMBER, "review"],
+        ["repair", EMBER, "repair"],
+    ]

Codegraph context: index_state: fresh; checked_at: 2026-11-14T23:20:38Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b: this task changes no existing symbol; the files it creates are new, so there are no dependents outside the diff.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
