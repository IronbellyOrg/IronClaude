15268669a5cd87378388c6636fdf9c56fc3fc3b6
Review one task for spec compliance.

Task brief: ## Task 12: Write the clock, the reviewer script and the hang guard

Depends on: Task 11

Follow `RL/IMPLEMENTATION.md` step 5 and `RL/DESIGN.md` sections 3.3, 9.2 to 9.4 and 10.2. Check that `RL/results/import-time.md` from Task 1 exists first. If `scaffold/clock.py` and `bin/run-reviewer.sh` are `built-local`, write them to the contract of `SW/DESIGN.md` 11.1 and 11.4 (read only): `scaffold/clock.py` with `hang_s`, `breakeven_row_cost` and `lens_row_cap` imported from `rl/lens.py`; `bin/run-reviewer.sh` with one attempt, `NOFALLBACK=1` required, brief from a file on stdin, `cd /tmp/evalsb-recipe/<doc>/repo`, hang-guard `timeout`, the model-identity check, `BLOCK_OK` by `FND.parse_block` after H2 on a temporary copy (a missing `ledger-v1` block does not make it false), `hang_s`, `killed` and `prompt_sha256` in `meta.json`, read-only tools (`--disallowedTools Edit Write NotebookEdit`, K4).

Write `RL/tests/test_hang_guard.py::test_formula_per_panel` (primary RL at b 100/120/122: 192/222/225 s; primary Z0: 150/180/183; haiku RL at 220/238: 375/402; sonnet RL at 259/302: 433.5/498), `RL/tests/test_clock.py` (`test_panel_elapsed_rl_and_other_arms`, `test_clock_starts_before_lens_render`, `test_reask_seconds_inside_the_clock`; REQ-29) and `RL/tests/test_report.py::test_breakeven_values` (`breakeven_row_cost(100, 14)` is 2.07, `(100, 12)` is 2.42, 120 gives 2.57, 122 gives 2.62, 116 gives 2.47; REQ-31 breakeven part).

Acceptance criteria (ids added by the orchestrator, in source order):
T12.AC1: `$T $RL/tests/test_hang_guard.py $RL/tests/test_clock.py $RL/tests/test_report.py -q -k "formula or panel_elapsed or clock or breakeven"` exits 0.
T12.AC2: `bin/run-reviewer.sh` refuses (exit 4) when `NOFALLBACK` is not set or the model is outside the allowlist.
T12.AC3: No reviewer script names `claude-opus-5-5` (K2).

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


Start sha: 15268669a5cd87378388c6636fdf9c56fc3fc3b6
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/run-reviewer.sh b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/run-reviewer.sh
new file mode 100755
index 000000000..a6c534394
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/run-reviewer.sh
@@ -0,0 +1,104 @@
+#!/usr/bin/env bash
+# usage: run-reviewer.sh <RUN dir> <doc id> <reviewer id> <model> <brief file> <hang_s> [<used_s>]
+# One reviewer, one attempt, in a fresh `claude -p` session in the sandbox repo SB/<doc>/repo (DESIGN 9.2, SWD 11.1).
+# Built locally to the sibling's written contract. No model ladder, no second attempt (DD-8): NOFALLBACK=1 is required.
+# The brief is read from the file on stdin. The call runs under `timeout <hang_s - used_s>` (hang guard, REQ-30);
+# used_s is what the panel clock has already used (default 0). Tools are read-only for files (K4).
+#
+# Writes RUN/reviews/<rid>.attempt1.{json,err,md,meta.json}, <rid>.{md,meta.json,cost.json}. meta.json holds
+#   status (ok | killed | invalid | error), killed, invalid and error (booleans that agree with status), model_ok,
+#   findings_block / block_ok (FND.parse_block ok after H2 on a temporary copy; a missing ledger-v1 block is not
+#   a block error), hang_s, prompt_sha256, wall_s, exit, reviewer_id, expected_model, observed_model, tokens.
+# Exit codes: 0 a meta.json was written (whatever its status); 2 usage error or no sandbox repo; 4 refused
+# (NOFALLBACK not 1, a model outside the allowlist, or the sibling's sandbox root).
+set -u -o pipefail
+HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
+# shellcheck source=rl-env.sh
+source "$HERE/rl-env.sh"
+# shellcheck source=common.sh
+source "$HERE/common.sh"
+
+if [ $# -lt 6 ] || [ $# -gt 7 ]; then
+  echo "usage: run-reviewer.sh <RUN dir> <doc id> <reviewer id> <model> <brief file> <hang_s> [<used_s>]" >&2
+  exit 2
+fi
+RUN=$1 DOC=$2 RID=$3 MODEL=$4 BRIEF=$5 HANG_S=$6 USED_S=${7:-0}
+
+sw_assert_nofallback || exit 4
+sw_assert_model "$MODEL" || exit 4
+NUM='^[0-9]+(\.[0-9]+)?$'
+[[ $HANG_S =~ $NUM ]] && [[ $USED_S =~ $NUM ]] || { echo "E_USAGE: hang_s and used_s are numbers" >&2; exit 2; }
+[[ $DOC =~ ^[A-Za-z0-9._-]+$ && $RID =~ ^[A-Za-z0-9._-]+$ ]] || { echo "E_USAGE: bad doc or reviewer id" >&2; exit 2; }
+[ -f "$BRIEF" ] || { echo "E_USAGE: no brief file $BRIEF" >&2; exit 2; }
+BRIEF=$(realpath -- "$BRIEF") # the call runs after a cd into the sandbox repo
+REPO_SB=$SB/$DOC/repo
+[ -d "$REPO_SB" ] || { echo "E_USAGE: no sandbox repo $REPO_SB" >&2; exit 2; }
+sw_assert_writable "$RUN" || exit 2
+
+OUT=$RUN/reviews
+mkdir -p "$OUT"
+A=$OUT/$RID.attempt1
+PROMPT_SHA=$(sha256sum "$BRIEF" | cut -d' ' -f1)
+LEFT=$(awk -v h="$HANG_S" -v u="$USED_S" 'BEGIN { r = h - u; if (r < 0.1) r = 0.1; printf "%.3f", r }')
+
+S=$(sw_now)
+(cd "$REPO_SB" && timeout --kill-after=2 "$LEFT" claude -p --model "$MODEL" --output-format json --no-session-persistence \
+  --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <"$BRIEF") >"$A.json" 2>"$A.err"
+RC=$?
+WALL=$(awk -v s="$S" -v e="$(sw_now)" 'BEGIN { printf "%.3f", e - s }')
+
+KILLED=false
+{ [ "$RC" -eq 124 ] || [ "$RC" -eq 137 ]; } && KILLED=true
+jq -r '[.[]|select(.type=="result")|.result]|.[0] // ""' "$A.json" >"$A.md" 2>/dev/null || : >"$A.md"
+OBS=$(jq -r '[.[]|select(.type=="assistant" and (.parent_tool_use_id==null))|.message.model]|unique|join(",")' "$A.json" 2>/dev/null)
+TOK=$(jq '[.[]|select(.type=="result")|.usage.output_tokens]|.[0] // 0' "$A.json" 2>/dev/null)
+TOKALL=$(jq '[.[]|select(.type=="result")|.modelUsage|to_entries[]|.value.outputTokens]|add // 0' "$A.json" 2>/dev/null)
+APIERR=false
+grep -q 'API Error' "$A.md" 2>/dev/null && APIERR=true
+LOWOBS=$(echo "$OBS" | tr 'A-Z' 'a-z')
+LOWEXP=$(echo "$MODEL" | tr 'A-Z' 'a-z')
+MODEL_OK=false
+if [ -n "$OBS" ] && [ "$OBS" != "<synthetic>" ] && { [ "$LOWOBS" = "$LOWEXP" ] || [ "$LOWOBS" = "$LOWEXP-build" ]; }; then
+  MODEL_OK=true
+fi
+
+# BLOCK_OK: the findings block parses with FND.parse_block after H2, on a temporary copy (the report stays raw)
+BLOCK_OK=false
+if [ -s "$A.md" ]; then
+  TMP=$(mktemp -d "${TMPDIR:-/tmp}/rl-block.XXXXXXXX") || exit 2
+  trap 'rm -rf "$TMP"' EXIT
+  cp "$A.md" "$TMP/in.md"
+  BLOCK_OK=$(sw_py -I -B -c '
+import sys
+sys.path.insert(0, sys.argv[1])
+from pathlib import Path
+from scaffold import normalise
+tmp = Path(sys.argv[2])
+try:
+    print("true" if normalise.normalise_file(tmp / "in.md", tmp / "out", "r")["ok"] else "false")
+except Exception:
+    print("false")
+' "$SW" "$TMP" 2>/dev/null) || BLOCK_OK=false
+  [ "$BLOCK_OK" = true ] || BLOCK_OK=false
+fi
+
+STATUS=ok INVALID=false ERROR=false
+if $KILLED; then
+  STATUS=killed
+elif [ "$RC" -ne 0 ] || $APIERR || [ ! -s "$A.md" ]; then
+  STATUS=error ERROR=true
+elif ! $MODEL_OK || ! $BLOCK_OK; then
+  STATUS=invalid INVALID=true
+fi
+
+jq -n --arg rid "$RID" --arg exp "$MODEL" --arg obs "$OBS" --argjson mok "$MODEL_OK" --argjson bok "$BLOCK_OK" \
+  --argjson w "$WALL" --argjson tok "${TOK:-0}" --argjson tokall "${TOKALL:-0}" --argjson rc "$RC" \
+  --argjson hang "$HANG_S" --argjson killed "$KILLED" --argjson invalid "$INVALID" --argjson err "$ERROR" \
+  --arg status "$STATUS" --arg sha "$PROMPT_SHA" '{
+    reviewer_id: $rid, expected_model: $exp, observed_model: $obs, model_ok: $mok,
+    findings_block: $bok, block_ok: $bok, attempt: 1, wall_s: $w, output_tokens_main: $tok,
+    output_tokens_all: $tokall, exit: $rc, hang_s: $hang, status: $status, killed: $killed,
+    invalid: $invalid, error: $err, prompt_sha256: $sha}' >"$A.meta.json"
+cp "$A.md" "$OUT/$RID.md"
+cp "$A.meta.json" "$OUT/$RID.meta.json"
+jq '{attempts: 1, total_wall_s: .wall_s, total_output_tokens_all: .output_tokens_all}' "$A.meta.json" >"$OUT/$RID.cost.json"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/scaffold/clock.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/scaffold/clock.py
new file mode 100644
index 000000000..c6e64e603
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/scaffold/clock.py
@@ -0,0 +1,118 @@
+"""The panel clock and the hang guard arithmetic (DESIGN 9.3, 9.4, 10.2; contract SWD 11.4 and 11.5).
+
+Built locally to the sibling's written contract (config/shared-manifest.json: `built-local`). Pure functions: no wall
+clock is read here, the launcher passes its monotonic stamps in. The row cap is `lens_row_cap` of rl/lens.py and is
+re-exported so the launcher has one import for the arithmetic.
+
+    hang_s(b, arm, panel)            1.5 * (b + expected overhead), counted from t0 (REQ-30)
+    breakeven_row_cost(b, rows)      seconds per ledger row at which the arm still meets the +35% rule (REQ-31)
+    panel_elapsed_s(...)             RL: end of R3 minus t0; other arms: last reviewer end minus t0 (REQ-29)
+    timing_record(...)               the fields of timing.json (DESIGN 9.3)
+"""
+
+from __future__ import annotations
+
+from fractions import Fraction
+
+from rl.lens import lens_row_cap, values
+
+__all__ = [
+    "ARMS",
+    "breakeven_row_cost",
+    "expected_overhead",
+    "hang_s",
+    "lens_row_cap",
+    "panel_elapsed_s",
+    "slowest_reviewer_s",
+    "timing_record",
+]
+
+ARMS = ("Z0-raw", "Z0", "K", "RL")
+HANG_FACTOR = 1.5
+
+
+def _arm(arm: str) -> str:
+    if arm not in ARMS:
+        raise ValueError(f"unknown arm {arm!r}; expected one of {ARMS}")
+    return arm
+
+
+def expected_overhead(arm: str, panel: str) -> float:
+    """Seconds the arm adds to the slowest reviewer: RL 28 s (primary) or 30 s (haiku, sonnet); 0 for Z0, K, Z0-raw."""
+    if _arm(arm) != "RL":
+        return 0
+    return values()["overhead_s"][panel]
+
+
+def hang_s(b: float, arm: str, panel: str) -> float:
+    """The hang guard in seconds from t0: 1.5 * (b + expected overhead of the arm)."""
+    return HANG_FACTOR * (b + expected_overhead(arm, panel))
+
+
+def breakeven_row_cost(b: float, rows: int) -> float:
+    """Seconds per ledger row, to 2 places, at which RL ends exactly at 1.35 b (DESIGN 10.2).
+
+    `0.35 b - 6` seconds are left for the rows (6 = render 1 + reading the recipes 4 + check 1); with `rows` rows the
+    cost per row is that divided by `rows`: 29 / 14 = 2.07 at b 100.
+    """
+    k = values()["row_cap"]
+    left = Fraction(str(k["share"])) * Fraction(str(b)) - Fraction(str(k["fixed_s"]))
+    return round(float(left / rows), 2)
+
+
+def slowest_reviewer_s(rev_start: dict, rev_end: dict) -> float:
+    """max over reviewers of rev_end - rev_start: the quantity b is a median of, for Z0."""
+    return round(max(rev_end[r] - rev_start[r] for r in rev_end), 3)
+
+
+def panel_elapsed_s(
+    arm: str, t0: float, rev_end: dict, r3_end: float | None = None
+) -> float:
+    """RL: the end of R3 (check and the ember re-ask included) minus t0. Other arms: the last reviewer end minus t0.
+    H2, the merge, the judge and the optional verifier are outside the clock in every arm."""
+    if _arm(arm) == "RL":
+        if r3_end is None:
+            raise ValueError("arm RL needs r3_end, the end of the ledger check")
+        return round(r3_end - t0, 3)
+    return round(max(rev_end.values()) - t0, 3)
+
+
+def timing_record(
+    arm: str,
+    t0: float,
+    rev_start: dict,
+    rev_end: dict,
+    render_s: float = 0,
+    check_s: float = 0,
+    reask_s: float = 0,
+    r3_end: float | None = None,
+) -> dict:
+    """The fields of timing.json (DESIGN 9.3). All stamps are one monotonic clock; t0 is taken before the lens render.
+
+    Refused: a reviewer that starts before t0 (the clock began after the render) or, for RL, before t0 + render_s;
+    an RL r3_end before the last reviewer ended; render, check or re-ask seconds on an arm that has none.
+    """
+    rl = _arm(arm) == "RL"
+    if not rl and (render_s or check_s or reask_s):
+        raise ValueError(f"arm {arm} has no render, check or re-ask seconds")
+    earliest = t0 + render_s
+    for rid, start in rev_start.items():
+        if start < earliest - 1e-9:
+            raise ValueError(
+                f"reviewer {rid} started at {start}, before t0 + render_s = {earliest}: the clock must start "
+                "before the lens render"
+            )
+        if rev_end[rid] < start:
+            raise ValueError(f"reviewer {rid} ended before it started")
+    if rl and r3_end is not None and r3_end < max(rev_end.values()) - 1e-9:
+        raise ValueError("r3_end is before the last reviewer ended")
+    return {
+        "t0": t0,
+        "render_s": render_s,
+        "rev_start": dict(rev_start),
+        "rev_end": dict(rev_end),
+        "check_s": check_s,
+        "reask_s": reask_s,
+        "panel_elapsed_s": panel_elapsed_s(arm, t0, rev_end, r3_end),
+        "slowest_reviewer_s": slowest_reviewer_s(rev_start, rev_end),
+    }
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_clock.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_clock.py
new file mode 100644
index 000000000..c2d82b083
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_clock.py
@@ -0,0 +1,72 @@
+"""REQ-29 at the level of the clock module (DESIGN 9.3).
+
+Task 13 completes two of the three tests at launcher level: `test_clock_starts_before_lens_render` (the launcher
+takes t0 before it calls the lens render) and `test_reask_seconds_inside_the_clock` (the launcher stamps r3_end after
+the ember re-ask). Here the arithmetic is pinned: what the module accepts and what `panel_elapsed_s` counts.
+"""
+
+import pytest
+
+from scaffold import clock
+
+START = {"r1": 1.0, "r2": 1.0, "r3": 1.0}
+END = {"r1": 81.0, "r2": 126.0, "r3": 127.0}
+
+
+def test_panel_elapsed_rl_and_other_arms():
+    # RL: the end of R3 minus t0, whatever the reviewers did; the other arms: the last reviewer end minus t0
+    assert clock.panel_elapsed_s("RL", 0.0, END, r3_end=128.0) == 128.0
+    assert clock.panel_elapsed_s("RL", 10.0, END, r3_end=128.0) == 118.0
+    for arm in ("Z0-raw", "Z0", "K"):
+        assert clock.panel_elapsed_s(arm, 0.0, END) == 127.0
+        assert clock.panel_elapsed_s(arm, 0.0, END, r3_end=500.0) == 127.0
+    with pytest.raises(ValueError, match="r3_end"):
+        clock.panel_elapsed_s("RL", 0.0, END)
+
+
+def test_slowest_reviewer_is_end_minus_start():
+    assert clock.slowest_reviewer_s(START, END) == 126.0
+
+
+def test_clock_starts_before_lens_render():
+    # RL: t0 = 0, the render takes 1 s, reviewers start at 1: the render is inside panel_elapsed_s
+    rec = clock.timing_record(
+        "RL", 0.0, START, END, render_s=1.0, check_s=1.0, r3_end=128.0
+    )
+    assert rec["panel_elapsed_s"] == 128.0
+    assert (
+        rec["panel_elapsed_s"] - rec["slowest_reviewer_s"] == 2.0
+    )  # render 1 s + check 1 s
+    # a clock that began after the render (t0 = 1, reviewers starting at 1 with render_s 1) is refused
+    with pytest.raises(ValueError, match="before the lens render"):
+        clock.timing_record("RL", 1.0, START, END, render_s=1.0, r3_end=128.0)
+    # a reviewer may not start before t0
+    with pytest.raises(ValueError, match="before t0"):
+        clock.timing_record("Z0", 2.0, START, END)
+
+
+def test_reask_seconds_inside_the_clock():
+    # ember ends at 81 s and is re-asked for 25 s; luna ends at 127 s; check 1 s: the re-ask is off the critical path
+    rec = clock.timing_record(
+        "RL", 0.0, START, END, render_s=1.0, check_s=1.0, reask_s=25.0, r3_end=128.0
+    )
+    assert rec["reask_s"] == 25.0
+    assert rec["check_s"] == 1.0  # check_s excludes the re-ask
+    # ember last: it ends at 140 after its own re-ask, and panel_elapsed_s grows with the re-ask seconds
+    late = dict(END, r1=140.0)
+    slow = clock.timing_record(
+        "RL", 0.0, START, late, render_s=1.0, check_s=1.0, reask_s=25.0, r3_end=167.0
+    )
+    assert slow["panel_elapsed_s"] == 167.0 > rec["panel_elapsed_s"]
+    # r3_end before a reviewer ended is a stamp from the wrong clock
+    with pytest.raises(ValueError, match="r3_end"):
+        clock.timing_record("RL", 0.0, START, END, render_s=1.0, r3_end=100.0)
+
+
+def test_other_arms_have_no_render_check_or_reask_seconds():
+    rec = clock.timing_record("Z0", 0.0, START, END)
+    assert (rec["render_s"], rec["check_s"], rec["reask_s"]) == (0, 0, 0)
+    assert rec["panel_elapsed_s"] == 127.0
+    for field in ("render_s", "check_s", "reask_s"):
+        with pytest.raises(ValueError, match="no render"):
+            clock.timing_record("K", 0.0, START, END, **{field: 1.0})
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_hang_guard.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_hang_guard.py
new file mode 100644
index 000000000..6429841cb
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_hang_guard.py
@@ -0,0 +1,47 @@
+"""REQ-30: the hang guard is 1.5 x (b + expected overhead) from t0 (DESIGN 9.4). The bin side (the `timeout` and the
+`killed` field) is tested in test_run_reviewer.py; the launcher side comes with Task 13."""
+
+import pytest
+from helpers import SW
+
+from rl import lens
+from scaffold import clock
+
+# DESIGN 9.4 table, written out by hand: (arm, panel, b) -> hang_s
+TABLE = [
+    ("RL", "primary", 100, 192),
+    ("RL", "primary", 120, 222),
+    ("RL", "primary", 122, 225),
+    ("Z0", "primary", 100, 150),
+    ("Z0", "primary", 120, 180),
+    ("Z0", "primary", 122, 183),
+    ("RL", "haiku", 220, 375),
+    ("RL", "haiku", 238, 402),
+    ("RL", "sonnet", 259, 433.5),
+    ("RL", "sonnet", 302, 498),
+]
+
+
+@pytest.mark.parametrize(("arm", "panel", "b", "expected"), TABLE)
+def test_formula_per_panel(arm, panel, b, expected):
+    assert clock.hang_s(b, arm, panel) == expected
+
+
+def test_table_b_values_are_the_planning_values():
+    b = lens.values(SW / "config" / "values.json")["b"]
+    for _arm, panel, value, _ in TABLE:
+        assert value in b[panel].values(), (panel, value)
+
+
+def test_overhead_is_28_30_30_for_rl_and_zero_for_the_other_arms():
+    assert [
+        clock.expected_overhead("RL", p) for p in ("primary", "haiku", "sonnet")
+    ] == [28, 30, 30]
+    for arm in ("Z0-raw", "Z0", "K"):
+        assert clock.expected_overhead(arm, "primary") == 0
+        assert clock.hang_s(100, arm, "primary") == 150
+
+
+def test_unknown_arm_is_refused():
+    with pytest.raises(ValueError, match="unknown arm"):
+        clock.hang_s(100, "RLx", "primary")
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_report.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_report.py
new file mode 100644
index 000000000..a7482da31
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_report.py
@@ -0,0 +1,28 @@
+"""REQ-31 (break-even part): the break-even row cost of DESIGN 10.2. Task 15 adds the report tests of the analysis."""
+
+import pytest
+
+from rl import lens
+from scaffold import clock
+
+
+@pytest.mark.parametrize(
+    ("b", "rows", "expected"),
+    [
+        (100, 14, 2.07),
+        (100, 12, 2.42),
+        (120, 14, 2.57),
+        (122, 14, 2.62),
+        (116, 14, 2.47),
+    ],
+)
+def test_breakeven_values(b, rows, expected):
+    assert clock.breakeven_row_cost(b, rows) == expected
+    assert clock.breakeven_row_cost(b=b, rows=rows) == expected
+
+
+def test_breakeven_agrees_with_the_row_cap():
+    # at b 100 the budget left for rows is 0.35 * 100 - 6 = 29 s: 14 rows fit at 2.07 s, 12 rows at 2.41 s
+    assert lens.lens_row_cap(100, 2.07, 14) == 14
+    assert lens.lens_row_cap(100, 2.41, 14) == 12
+    assert clock.lens_row_cap is lens.lens_row_cap
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_run_reviewer.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_run_reviewer.py
new file mode 100644
index 000000000..824cd7caf
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_run_reviewer.py
@@ -0,0 +1,258 @@
+"""bin/run-reviewer.sh against the fake claude (DESIGN 9.2, 8 row 6, REQ-30): one attempt, the refusals, the hang guard,
+the meta.json keys and their agreement with rl.rowcheck._dropped. No model starts."""
+
+import hashlib
+import json
+import os
+import subprocess
+import time
+
+import pytest
+import rl_support as s
+from conftest import FAKES
+from helpers import SW
+
+from rl import render, rowcheck
+from scaffold import fnd
+
+pytestmark = pytest.mark.slow
+
+SCRIPT = SW / "bin" / "run-reviewer.sh"
+EMBER, SONNET = "muse-ember-1.0", "claude-sonnet-5-5"
+DOC, RID = "doc1", "S"
+KEYS = {
+    "reviewer_id",
+    "expected_model",
+    "observed_model",
+    "model_ok",
+    "findings_block",
+    "block_ok",
+    "attempt",
+    "wall_s",
+    "output_tokens_main",
+    "output_tokens_all",
+    "exit",
+    "hang_s",
+    "status",
+    "killed",
+    "invalid",
+    "error",
+    "prompt_sha256",
+}
+
+
+@pytest.fixture
+def box(tmp_roots):
+    """A sandbox repo under SW_SB_ROOT, a candidate, an ember brief file and a run folder."""
+    root = tmp_roots.root
+    (tmp_roots.sb / DOC / "repo").mkdir(parents=True)
+    cand = root / "candidate.md"
+    cand.write_text(
+        (SW / "fixtures" / "plans" / "p_basic.md").read_text(encoding="utf-8"),
+        encoding="utf-8",
+    )
+    text = render.brief(
+        s.roles("primary")["S"], {"cand_sb": str(cand), "sha": s.SHA}, s.SOURCE
+    )["text"]
+    brief = root / "brief.txt"
+    brief.write_text(text, encoding="utf-8")
+    tmp = root / "tmp"
+    tmp.mkdir()
+    tmp_roots.env["TMPDIR"] = str(tmp)
+    tmp_roots.brief, tmp_roots.run, tmp_roots.tmp = brief, root / "run", tmp
+    return tmp_roots
+
+
+def run(box, scenario="ok", model=EMBER, hang="60", used="0", env=None, drop=()):
+    env = env or {}
+    if (
+        "PATH" in env
+    ):  # the spy test puts a wrapper of the fake first; with_env would refuse that
+        e = dict(box.env, FAKE_SCENARIO=scenario, **env)
+    else:
+        e = box.with_env(FAKE_SCENARIO=scenario, **env)
+    for k in drop:
+        e.pop(k, None)
+    args = [str(SCRIPT), str(box.run), DOC, RID, model, str(box.brief), hang]
+    return subprocess.run(
+        ["bash", *args, *([used] if used != "0" else [])],
+        capture_output=True,
+        text=True,
+        env=e,
+        timeout=60,
+    )
+
+
+def meta(box):
+    return json.loads((box.run / "reviews" / f"{RID}.meta.json").read_text())
+
+
+def calls(box):
+    return box.call_log.read_text().splitlines() if box.call_log.exists() else []
+
+
+def test_ok_run_writes_the_files_and_the_keys(box):
+    r = run(box)
+    assert r.returncode == 0, r.stderr
+    m = meta(box)
+    assert set(m) == KEYS
+    assert (m["status"], m["killed"], m["invalid"], m["error"]) == (
+        "ok",
+        False,
+        False,
+        False,
+    )
+    assert (m["model_ok"], m["block_ok"], m["findings_block"]) == (True, True, True)
+    assert m["prompt_sha256"] == hashlib.sha256(box.brief.read_bytes()).hexdigest()
+    assert (m["hang_s"], m["attempt"], m["exit"], m["expected_model"]) == (
+        60,
+        1,
+        0,
+        EMBER,
+    )
+    assert m["observed_model"] == EMBER and m["wall_s"] >= 0
+    rev = box.run / "reviews"
+    for name in (
+        "attempt1.json",
+        "attempt1.err",
+        "attempt1.md",
+        "attempt1.meta.json",
+        "md",
+        "meta.json",
+        "cost.json",
+    ):
+        assert (rev / f"{RID}.{name}").is_file(), name
+    assert json.loads((rev / f"{RID}.cost.json").read_text())["attempts"] == 1
+    assert (rev / f"{RID}.md").read_text().startswith("review: 1 of 3")
+    assert len(calls(box)) == 1
+    assert (
+        list(box.tmp.glob("rl-block.*")) == []
+    )  # the temporary H2 copy is gone (uv leaves its own lock file)
+
+
+def test_one_attempt_cwd_and_read_only_flags(box, tmp_path):
+    spy = tmp_path / "spy"
+    spy.mkdir()
+    out = tmp_path / "spy.out"
+    (spy / "claude").write_text(
+        f'#!/usr/bin/env bash\n{{ pwd; echo "$@"; }} >>{out}\nexec {FAKES}/claude "$@"\n'
+    )
+    (spy / "claude").chmod(0o755)
+    r = run(box, env={"PATH": f"{spy}{os.pathsep}{box.env['PATH']}"})
+    assert r.returncode == 0, r.stderr
+    cwd, argv = out.read_text().splitlines()
+    assert cwd == str(box.sb / DOC / "repo")
+    assert f"-p --model {EMBER} --output-format json --no-session-persistence" in argv
+    assert (
+        "--permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit"
+        in argv
+    )
+
+
+def test_missing_ledger_block_is_not_a_block_error(box):
+    run(box, "ledger_missing")
+    m = meta(box)
+    assert (m["block_ok"], m["status"], m["invalid"]) == (True, "ok", False)
+
+
+def test_block_ok_is_decided_after_h2_and_the_report_stays_raw(box):
+    run(box, "long_anchor")
+    m = meta(box)
+    assert (m["block_ok"], m["status"]) == (True, "ok")
+    raw = json.loads((box.run / "reviews" / f"{RID}.attempt1.json").read_text())[-1][
+        "result"
+    ]
+    assert (
+        box.run / "reviews" / f"{RID}.md"
+    ).read_text() == raw + "\n"  # jq -r ends the text with a newline, as in RR
+    assert fnd.parse_block(raw)["ok"] is False  # it only parses after H2
+
+
+@pytest.mark.parametrize(
+    ("scenario", "status", "model_ok"),
+    [
+        ("bad_block", "invalid", True),
+        ("wrong_model", "invalid", False),
+        ("api_error", "error", False),
+        ("exit127", "error", False),
+    ],
+)
+def test_failures_are_recorded_and_agree_with_rowcheck(box, scenario, status, model_ok):
+    r = run(box, scenario)
+    assert r.returncode == 0, r.stderr
+    m = meta(box)
+    assert (m["status"], m["model_ok"]) == (status, model_ok)
+    assert (m["invalid"], m["error"], m["killed"]) == (
+        status == "invalid",
+        status == "error",
+        False,
+    )
+    assert rowcheck._dropped(box.run / "reviews", RID) is True
+    assert len(calls(box)) == 1  # one attempt, no retry
+
+
+def test_ok_is_not_dropped_by_rowcheck(box):
+    run(box)
+    assert rowcheck._dropped(box.run / "reviews", RID) is False
+
+
+def test_sleeping_reviewer_is_killed_by_the_guard(box):
+    t = time.monotonic()
+    r = run(box, "sleep", hang="1.5", env={"FAKE_SLEEP_S": "30"})
+    assert r.returncode == 0, r.stderr
+    assert time.monotonic() - t < 15
+    m = meta(box)
+    assert (m["status"], m["killed"], m["invalid"], m["error"]) == (
+        "killed",
+        True,
+        False,
+        False,
+    )
+    assert m["hang_s"] == 1.5 and m["exit"] in (124, 137)
+    assert rowcheck._dropped(box.run / "reviews", RID) is True
+    assert len(calls(box)) == 1
+
+
+def test_time_already_used_shortens_the_guard(box):
+    t = time.monotonic()
+    run(box, "sleep", hang="100", used="99", env={"FAKE_SLEEP_S": "30"})
+    assert time.monotonic() - t < 15
+    m = meta(box)
+    assert (m["status"], m["hang_s"]) == ("killed", 100)
+
+
+def test_refused_without_nofallback(box):
+    r = run(box, drop=("NOFALLBACK",))
+    assert r.returncode == 4 and "NOFALLBACK" in r.stderr
+    assert calls(box) == [] and not box.run.exists()
+
+
+def test_refused_for_a_model_outside_the_allowlist(box):
+    r = run(box, model="gpt-6.1-sol")
+    assert r.returncode == 4 and "E_MODEL" in r.stderr
+    assert calls(box) == [] and not box.run.exists()
+
+
+def test_refused_on_the_sibling_sandbox_root(box):
+    r = run(box, env={"SW_SB_ROOT": "/tmp/evalsb-sweep"})
+    assert r.returncode == 4 and calls(box) == []
+
+
+def test_usage_errors_exit_2(box):
+    assert (
+        subprocess.run(
+            ["bash", str(SCRIPT)], capture_output=True, env=box.env
+        ).returncode
+        == 2
+    )
+    assert run(box, hang="soon").returncode == 2
+    (box.brief).unlink()
+    assert run(box).returncode == 2
+
+
+def test_script_text_keeps_k2_and_k4():
+    text = SCRIPT.read_text()
+    assert "claude-opus-5-5" not in text
+    assert "--disallowedTools Edit Write NotebookEdit" in text
+    assert "NOFALLBACK" in text and "sw_assert_model" in text
+    assert SCRIPT.read_text().index("rl-env.sh") < SCRIPT.read_text().index("common.sh")

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
