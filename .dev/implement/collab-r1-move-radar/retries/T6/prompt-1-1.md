b6de60bca78d4bd884af1b3721cebe4d62c50bb9
Review one task for spec compliance.

Task brief: T6 (source: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/DESIGN.md; task grouping in .dev/implement/collab-r1-move-radar/tasks.md). Covers DESIGN.md section 1.2 row tools/launch.sh, section 1.3 rows spikes/gate0-check.sh and spikes/spike4.sh (gate0-check.sh was reviewed under T2), the kill switch of section 4, and sections 5.1 and 5.2 (interface, preflight, per-package steps, exit codes 0/1/2, launch.log).
T6.AC1: launch steps and exit codes of 5.1/5.2, and the kill switch of section 4 (PANEL_COLLAB read once by launch.sh, 0 or 1, default 1, any other value refused exit 2; no --settings, no hook, no msgs/ directory with 0; NOFALLBACK handling; values handling for collab 0 without values file).
T6.AC2: T-10 gate order (a fixture gate0.json lacking S3: collab 1 accepts rep 0 and refuses rep 1 with exit 2; without S0 both refused) and the launch parts of F-4 (leak -> QUARANTINED, skip merge and judge), F-5 (hook_calls 0 -> ALARM line in launch.log), F-10 (reviewers invalid -> package invalid, exit 1, no fallback model in any argv), F-11 (merge refuses -> package invalid, merge stdout kept), F-12 (judge fails once then succeeds: exactly two judge calls; always fails -> judge_failed) pass.
Notes from the task grouping: spikes/spike4.sh runs collab-0 rows and then values.py spike4; Spike 4 itself is not run in this session (orchestrator constraint). launch.sh test seams --root, --sb, --a1 and --prebuilt are for the tests only and change nothing in production defaults.
Global constraints: Orchestrator constraints (global): create and edit files only under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/ (plus .dev/implement/collab-r1-move-radar/ and scratch under /tmp/evalsb-collab-r1/ and /tmp/collab-r1/); do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder or any other redesign's folder; do not stage, commit or push; python only through uv; models allowed muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7, Opus only as the blind judge, never Qwen or glm; NOFALLBACK=1; no full panel runs; at most 3 reviewer or judge sessions at once.
Start sha: b6de60bca78d4bd884af1b3721cebe4d62c50bb9
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/spike4.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/spike4.sh
new file mode 100755
index 000000000..96b2819bf
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/spikes/spike4.sh
@@ -0,0 +1,17 @@
+#!/usr/bin/env bash
+# spike4.sh <panel> [<rep> <rep> <rep> ...]   (DESIGN.md 6.3, Spike 4)
+# Runs the collab-0 rows <panel>-c0-r<rep> one after another (default reps 1 2 3; each is a full row of three packages with
+# planning values and the 2.0 x planning-B hang guard), then writes values/<panel>/<pkg>.json with tools/values.py.
+# values.py refuses fewer than 3 rows and refuses to overwrite an existing values file. Not run by the implementation session:
+# it is nine reviewer sessions per rep.
+set -u -o pipefail
+TOOLS=$(cd "$(dirname "${BASH_SOURCE[0]}")/../tools" && pwd)
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+PANEL=${1:?usage: spike4.sh <panel> [<rep> ...]}; shift
+REPS=("$@"); [ ${#REPS[@]} -gt 0 ] || REPS=(1 2 3)
+ROWS=()
+for r in "${REPS[@]}"; do
+  PANEL_COLLAB=0 bash "$TOOLS/launch.sh" "$PANEL" "$r" || echo "spike4: row $PANEL-c0-r$r finished with a failing package" >&2
+  ROWS+=("$PANEL-c0-r$r")
+done
+cd "$REPO" && uv run python "$TOOLS/values.py" spike4 "$PANEL" "${ROWS[@]}"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_launch.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_launch.py
new file mode 100644
index 000000000..7d2b3ea2d
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_launch.py
@@ -0,0 +1,231 @@
+"""launch.sh (DESIGN.md 5.1, 5.2): T-10 gate order, the kill switch (AC-4) and the launch parts of F-4, F-5, F-10, F-11, F-12.
+
+The `claude` and `superclaude` executables are stubs on PATH (never the gateway). The real, unchanged judge-one.sh runs with the
+stub judge; it reads ground truth from the real A1DIR (read only) and writes into the tmp root through the relative-path trick.
+"""
+
+import json
+import os
+import shutil
+import subprocess
+
+import pytest
+from conftest import A1DIR, FIX, R1, REPO, TOOLS, finding, json_reply, report, run
+
+DS = "TASK-WF-designSpec-20261107-075614"
+
+CLAUDE = r"""#!/usr/bin/env bash
+D=${STUB_DIR:?}
+cat > "$D/stdin.$$"
+MODEL=; SETTINGS=
+for ((i = 1; i <= $#; i++)); do
+  case ${!i} in --model) j=$((i + 1)); MODEL=${!j};; --settings) j=$((i + 1)); SETTINGS=${!j};; esac
+done
+if [ "$MODEL" = claude-opus-5-5 ]; then  # the blind judge
+  n=$(( $(cat "$D/judge.count" 2>/dev/null || echo 0) + 1 )); echo "$n" > "$D/judge.count"
+  [ "$n" -le "${STUB_JUDGE_FAILS:-0}" ] && exit 1
+  p=$(grep -o 'Write JSON to [^ ]*score.json' "$D/stdin.$$" | head -1 | sed 's/^Write JSON to //')
+  cp "$D/score.body" "$p"; printf '[{"type":"result","result":"ok","session_id":"judge"}]\n'; exit 0
+fi
+if [ -n "${STUB_BAD_BOARD:-}" ] && [ -n "$SETTINGS" ]; then  # a leaking board line: an anchor key is not allowed in panel-msg/1
+  board=$(printf '%s' "$SETTINGS" | jq -r '.hooks.PostToolUse[0].hooks[0].command' | grep -o "'[^']*'" | head -1 | tr -d "'")
+  printf '{"v":"panel-msg/1","id":"m-x-06","run":"r","from":"radar","to":"t4-1","t":1,"kind":"move","move":"M3","anchor":"x"}\n' >> "$board/msgs/radar.jsonl"
+fi
+[ -n "${STUB_REVIEWER_EXIT:-}" ] && exit "$STUB_REVIEWER_EXIT"
+sed "s/@@MODEL@@/$MODEL/g" "$D/reply"
+"""
+
+SUPERCLAUDE = r"""#!/usr/bin/env bash
+out=; led=; reps=()
+for ((i = 1; i <= $#; i++)); do
+  case ${!i} in --out) j=$((i + 1)); out=${!j};; --ledger) j=$((i + 1)); led=${!j};; --report) j=$((i + 1)); reps+=("${!j}");; esac
+done
+touch "${STUB_DIR:?}/merge.called"
+[ -n "${STUB_MERGE_RC:-}" ] && { echo "merge refused: no valid findings block"; exit "$STUB_MERGE_RC"; }
+echo '{"rows":[{},{},{}]}' > "$led"
+{ echo "verdict: FAIL"; for r in "${reps[@]}"; do echo "report ${r#*=} (${r%%=*})"; done; } > "$out"
+"""
+
+
+class L:
+    """A tmp R1 root with one prebuilt fixture sandbox for the DS package, stub executables and a launch() helper."""
+
+    def __init__(self, tmp_path, root):
+        self.root, self.tmp = root, tmp_path
+        self.sb = tmp_path / "sb"
+        repo = self.sb / DS / "repo"
+        (repo / "src").mkdir(parents=True)
+        (repo / "src" / "a.py").write_text("x\n")
+        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
+        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
+        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "s"], cwd=repo, check=True)
+        cand = self.sb / "cand" / DS
+        cand.mkdir(parents=True)
+        shutil.copy(FIX / "cand" / "candidate.md", cand / "candidate.md")
+        (cand / "source.md").write_text("# source\n")
+        (root / "index").mkdir()
+        shutil.copy(FIX / "index.json", root / "index" / f"{DS}.json")
+        self.set_gates(S3=False)
+        vals = run(["uv", "run", "python", str(TOOLS / "values.py"), "show", "el2", DS, "--root", str(root)]).stdout
+        v = root / "values" / "el2" / f"{DS}.json"
+        v.parent.mkdir(parents=True)
+        v.write_text(vals)
+        import hashlib
+        (v.parent / f"{DS}.json.sha256").write_text(hashlib.sha256(vals.encode()).hexdigest() + f"  {DS}.json\n")
+        self.stub = tmp_path / "stub"
+        self.bin = tmp_path / "bin"
+        self.stub.mkdir()
+        self.bin.mkdir()
+        for name, body in (("claude", CLAUDE), ("superclaude", SUPERCLAUDE)):
+            (self.bin / name).write_text(body)
+            (self.bin / name).chmod(0o755)
+        (self.stub / "reply").write_text(json_reply(report(finding())))
+        (self.stub / "score.body").write_text(json.dumps({"label": "R", "gt_covered_any": ["GT2"], "gt_covered_blocking": [],
+                                                          "ledger_rows_total": 3, "wrong_blockers": 0}))
+        home = tmp_path / "home"
+        home.mkdir()
+        self.env = dict(os.environ, PATH=f"{self.bin}:{os.environ['PATH']}", STUB_DIR=str(self.stub), HOME=str(home))
+        self.env.pop("NOFALLBACK", None)
+        self.env.pop("PANEL_COLLAB", None)
+
+    def set_gates(self, S0=True, S2=True, S3=True):
+        g = {"G-BASE": "pass", "G-PINS": "pass", "S0": "pass" if S0 else "missing", "S2": "pass" if S2 else "missing",
+             "S3": "pass" if S3 else "missing", "Spike 4": "pass", "REQ-S3": "recorded"}
+        (self.root / "spikes").mkdir(exist_ok=True)
+        (self.root / "spikes" / "gate0.json").write_text(json.dumps(g))
+
+    def launch(self, collab=1, rep=0, panel="el2", **env):
+        e = dict(self.env, PANEL_COLLAB=str(collab), **{k: str(v) for k, v in env.items()})
+        return run(["bash", str(TOOLS / "launch.sh"), "--root", str(self.root), "--sb", str(self.sb), "--prebuilt", panel, str(rep), DS],
+                   env=e, timeout=400)
+
+    def d(self, row):
+        return self.root / "runs" / row / DS
+
+    def status(self, row):
+        return (self.d(row) / "status").read_text().strip()
+
+    def log(self, row):
+        return (self.root / "runs" / row / "launch.log").read_text()
+
+    def judge_calls(self):
+        p = self.stub / "judge.count"
+        return int(p.read_text()) if p.exists() else 0
+
+
+@pytest.fixture
+def lenv(tmp_path, root):
+    return L(tmp_path, root)
+
+
+# ---------------------------------------------------------------- T-10 gate order (AC-2)
+def test_gate_order_s3_blocks_only_rep_ge_1(lenv):
+    r = lenv.launch(collab=1, rep=1)
+    assert r.returncode == 2 and "S3" in r.stderr and not (lenv.root / "runs" / "el2-c1-r1" / "launch.log").exists()
+    r = lenv.launch(collab=1, rep=0)  # the smoke row (rep 0) needs only G-BASE, G-PINS, S0, S2 and the values file
+    assert r.returncode == 0, r.stdout + r.stderr
+    assert "START" in lenv.log("el2-c1-r0") and lenv.status("el2-c1-r0") == "ok"
+
+
+def test_gate_order_without_s0_refuses_both(lenv):
+    lenv.set_gates(S0=False, S3=False)
+    for rep in (0, 1):
+        r = lenv.launch(collab=1, rep=rep)
+        assert r.returncode == 2 and "S0" in r.stderr
+    assert lenv.launch(collab=0, rep=0).returncode == 0  # a collab-0 row needs only G-BASE and G-PINS
+
+
+# ---------------------------------------------------------------- preflight refusals (5.2 step 1)
+def test_preflight_refusals(lenv):
+    assert lenv.launch(collab=2).returncode == 2
+    assert lenv.launch(collab=0, NOFALLBACK=0).returncode == 2
+    shutil.rmtree(lenv.root / "values")
+    r = lenv.launch(collab=1, rep=0)
+    assert r.returncode == 2 and "Spike 4" in r.stderr
+    (lenv.root / "results").mkdir()
+    (lenv.root / "results" / "el2-c0-r0.json").write_text("{}")
+    assert lenv.launch(collab=0, rep=0).returncode == 2  # a finished row is never re-run
+    (lenv.root / "results" / "el2-c0-r0.json").unlink()
+    (lenv.root / "config" / "catalogue.json").write_text("{}")
+    r = lenv.launch(collab=0, rep=0)
+    assert r.returncode == 2 and "catalogue" in r.stderr
+
+
+# ---------------------------------------------------------------- kill switch (AC-4)
+def test_collab0_row_has_no_hooks_no_msgs_no_settings(lenv):
+    shutil.rmtree(lenv.root / "values")  # no values file yet (Spike 4 itself runs collab-0 rows): planning values, 2.0 x B hang guard
+    r = lenv.launch(collab=0, rep=0)
+    assert r.returncode == 0, r.stdout + r.stderr
+    d = lenv.d("el2-c0-r0")
+    assert not (d / "settings").exists() and not (d / "board" / "msgs").exists()
+    for m in (d / "reviews").glob("*.meta.json"):
+        if ".attempt" in m.name:
+            continue
+        assert all("--settings" not in a for a in json.loads(m.read_text())["argv"][0])
+    run_json = json.loads((d / "run.json").read_text())
+    assert run_json["values"] == "planning" and run_json["collab"] == 0
+    assert run_json["HANG_MS"] - run_json["T0_MS"] == 232_000  # 2.0 x planning B (116 s)
+    row = json.loads((lenv.root / "results" / "el2-c0-r0.json").read_text())
+    assert row["status"] == "incomplete" and row["collab_counters"]["injections"] == 0  # a one-package smoke is incomplete by design
+
+
+# ---------------------------------------------------------------- F-5 hook not firing
+def test_f5_hook_not_firing_alarm(lenv):
+    r = lenv.launch(collab=1, rep=0)
+    assert r.returncode == 0, r.stdout + r.stderr
+    assert "ALARM hook_calls=0 t2b-1" in lenv.log("el2-c1-r0")
+    settings = lenv.d("el2-c1-r0") / "settings"
+    assert sorted(p.name for p in settings.iterdir()) == ["t2b-1.json", "t3-1.json", "t4-1.json"]
+    ctx = lenv.d("el2-c1-r0") / "board" / "ctx"
+    assert json.loads((ctx / "panel.json").read_text())["readers"] == ["t4-1", "t3-1"] and (ctx / "index.json").exists()
+
+
+# ---------------------------------------------------------------- F-10 misroute / binary missing
+def test_f10_reviewers_invalid_no_merge_no_fallback(lenv):
+    r = lenv.launch(collab=0, rep=0, STUB_REVIEWER_EXIT=127)
+    assert r.returncode == 1
+    assert lenv.status("el2-c0-r0") == "invalid"
+    assert not (lenv.stub / "merge.called").exists() and lenv.judge_calls() == 0
+    expected = {"t2b-1": "muse-ember-1.0", "t4-1": "gpt-6-luna", "t3-1": "gpt-6-luna"}
+    for rid, model in expected.items():
+        meta = json.loads((lenv.d("el2-c0-r0") / "reviews" / f"{rid}.meta.json").read_text())
+        assert meta["valid"] is False and meta["attempts"] <= 2
+        for argv in meta["argv"]:
+            assert argv[argv.index("--model") + 1] == model
+    assert not list((lenv.root / "runs").rglob("fallback.log"))
+
+
+# ---------------------------------------------------------------- F-11 merge refuses
+def test_f11_merge_refused_keeps_stdout(lenv):
+    r = lenv.launch(collab=0, rep=0, STUB_MERGE_RC=1)
+    assert r.returncode == 1 and lenv.status("el2-c0-r0") == "invalid"
+    assert "merge refused" in (lenv.d("el2-c0-r0") / "merge-stdout.txt").read_text()
+    assert lenv.judge_calls() == 0
+
+
+# ---------------------------------------------------------------- F-12 judge failure
+def test_f12_judge_fails_once_then_succeeds(lenv):
+    r = lenv.launch(collab=0, rep=0, STUB_JUDGE_FAILS=1)
+    assert r.returncode == 0, r.stdout + r.stderr
+    assert lenv.judge_calls() == 2 and lenv.status("el2-c0-r0") == "ok"
+
+
+def test_f12_judge_always_fails(lenv):
+    r = lenv.launch(collab=0, rep=0, STUB_JUDGE_FAILS=9)
+    assert r.returncode == 1 and lenv.judge_calls() == 2 and lenv.status("el2-c0-r0") == "judge_failed"
+    row = json.loads((lenv.root / "results" / "el2-c0-r0.json").read_text())
+    assert row["packages"][DS]["status"] == "judge_failed" and row["status"] == "incomplete"
+
+
+# ---------------------------------------------------------------- F-4 leak -> quarantine -> no merge, no judge
+def test_f4_leaking_board_line_quarantines_package(lenv):
+    r = lenv.launch(collab=1, rep=0, STUB_BAD_BOARD=1)
+    assert r.returncode == 1
+    assert lenv.status("el2-c1-r0") == "quarantined" and (lenv.d("el2-c1-r0") / "QUARANTINED").exists()
+    assert not (lenv.stub / "merge.called").exists() and lenv.judge_calls() == 0
+
+
+def test_launch_order_mode_and_paths_exist():
+    assert subprocess.run(["bash", str(TOOLS / "launch.sh"), "--order", "t4-1", "reader"], capture_output=True, text=True).stdout.strip() \
+        == "M3,M5,M6,M9,M8,M10"
+    assert (A1DIR / "tools" / "tmp-scripts" / "judge-one.sh").exists() and R1.exists() and REPO.exists()
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh
index bc8f39128..a852fedae 100755
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/launch.sh
@@ -1,6 +1,10 @@
 #!/usr/bin/env bash
-# launch.sh: PANEL_COLLAB=<0|1> bash tools/launch.sh <panel> <rep> [<pkg> ...]   (DESIGN.md section 5)
+# launch.sh: PANEL_COLLAB=<0|1> bash tools/launch.sh [--root R1] [--sb SB] [--a1 A1DIR] [--prebuilt] <panel> <rep> [<pkg> ...]
 #            bash tools/launch.sh --order <rid> <searcher|reader>   (prints the receiver's move order, section 2.5)
+# One launch = one results row <panel>-c<collab>-r<rep> over the requested packages (default DS, AL, DE), DESIGN.md section 5.
+# Exit 0: row written and every requested package ok. 1: row written, some package invalid, quarantined or judge_failed.
+# 2: a preflight refusal (nothing run). Log: runs/<row>/launch.log. Never prompts.
+# --root/--sb/--a1/--prebuilt exist for the tests (--prebuilt: sandbox and index were built by the test, skip those two steps).
 set -u -o pipefail
 order() { # rotate the role list left by int(sha256(rid)[0:8], 16) mod len
   local rid=$1 role=$2 list h off i out=()
@@ -10,3 +14,134 @@ order() { # rotate the role list left by int(sha256(rid)[0:8], 16) mod len
   (IFS=,; echo "${out[*]}")
 }
 if [ "${1:-}" = --order ]; then order "$2" "$3"; exit 0; fi
+
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+TOOLS=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
+R1=$(dirname "$TOOLS")
+A1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
+SB=/tmp/evalsb-collab-r1
+PREBUILT=0
+refuse() { echo "REFUSE $*" >&2; exit 2; }
+POS=()
+while [ $# -gt 0 ]; do case $1 in
+  --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; --a1) A1=$2; shift 2;; --prebuilt) PREBUILT=1; shift;; *) POS+=("$1"); shift;;
+esac; done
+R1=$(realpath -m "$R1"); SB=$(realpath -m "$SB")
+[ ${#POS[@]} -ge 2 ] || refuse "usage: launch.sh [options] <panel> <rep> [<pkg> ...]"
+PANEL=${POS[0]}; REP=${POS[1]}; PKGS=("${POS[@]:2}")
+DS=TASK-WF-designSpec-20261107-075614; AL=TASK-WF-makeTheAliasOnly-20261105-051649; DE=TASK-WF-design-20261108-041415
+[ ${#PKGS[@]} -gt 0 ] || PKGS=($DS $AL $DE)
+
+# ---------------------------------------------------------------- 1. preflight
+COLLAB=${PANEL_COLLAB:-1}
+case $COLLAB in 0|1) ;; *) refuse "PANEL_COLLAB must be 0 or 1, got $COLLAB";; esac
+case $PANEL in el2|sl2|hl2) ;; *) refuse "panel must be el2, sl2 or hl2";; esac
+[[ $REP =~ ^[0-9]+$ ]] || refuse "rep must be a non-negative integer"
+for p in "${PKGS[@]}"; do case $p in $DS|$AL|$DE) ;; *) refuse "unknown package $p";; esac; done
+case ${NOFALLBACK:-1} in 1) ;; *) refuse "NOFALLBACK must be unset or 1";; esac
+export NOFALLBACK=1
+for c in claude jq flock uv superclaude sha256sum; do command -v "$c" >/dev/null 2>&1 || refuse "$c is not on PATH"; done
+M=$R1/manifest.json
+sha() { sha256sum "$1" | cut -d' ' -f1; }
+JUDGE=$A1/tools/tmp-scripts/judge-one.sh
+[ "$(jq -r .catalogue_sha256 "$M")" = "$(sha "$R1/config/catalogue.json")" ] || refuse "catalogue.json does not match its pin in manifest.json"
+[ "$(jq -r .brief_sha256 "$M")" = "$(sha "$R1/config/brief.txt")" ] || refuse "brief.txt does not match its pin in manifest.json"
+[ "$(jq -r .judge_one_sha256 "$M")" = "$(sha "$JUDGE")" ] || refuse "judge-one.sh does not match its pin in manifest.json"
+for p in "${PKGS[@]}"; do
+  jq -e --arg p "$p" '.base_commits[$p].sha|test("^[0-9a-f]{40}$")' "$M" >/dev/null 2>&1 || refuse "manifest.json has no base sha for $p"
+  if [ "$COLLAB" = 1 ]; then
+    V=$R1/values/$PANEL/$p.json
+    [ -f "$V" ] && [ "$(sha "$V")" = "$(cut -d' ' -f1 "$V.sha256" 2>/dev/null)" ] || refuse "PANEL_COLLAB=1 needs values/$PANEL/$p.json with a matching .sha256 (Spike 4)"
+  fi
+done
+gate() { jq -r --arg k "$1" '.[$k] // "missing"' "$R1/spikes/gate0.json" 2>/dev/null || echo missing; }
+NEED=(G-BASE G-PINS)
+[ "$COLLAB" = 1 ] && NEED+=(S0 S2)
+[ "$COLLAB" = 1 ] && [ "$REP" -ge 1 ] && NEED+=(S3)
+for g in "${NEED[@]}"; do [ "$(gate "$g")" = pass ] || refuse "Gate 0: $g is $(gate "$g"), not pass (gate order, DESIGN.md 6.3)"; done
+ROW=$PANEL-c$COLLAB-r$REP
+[ ! -f "$R1/results/$ROW.json" ] || refuse "row $ROW is finished (results/$ROW.json exists)"
+mkdir -p "$R1/runs/$ROW"
+LOG=$R1/runs/$ROW/launch.log
+log() { printf '%s %s %s\n' "$(date -u +%FT%TZ)" "$1" "${*:2}" >> "$LOG"; }
+[ -f "$R1/runs/$ROW/run.json" ] || jq -n -c --arg row "$ROW" --arg panel "$PANEL" --argjson c "$COLLAB" --argjson rep "$REP" --arg t "$(date -u +%FT%TZ)" \
+  '{row:$row,panel:$panel,collab:$c,rep:$rep,started_utc:$t}' > "$R1/runs/$ROW/run.json"
+
+# ---------------------------------------------------------------- 2-7. per package
+CFG=$R1/config/panels.json
+py() { (cd "$REPO" && uv run python "$@"); }
+run_package() { # run_package <pkg>; writes runs/<row>/<pkg>/status
+  local pkg=$1 d=$R1/runs/$ROW/$1 t0 dl rid role model cp1 cp2 k ord fin guard rc n=0 any_bad=0 spec
+  [ -f "$d/status" ] && { log SKIP "$pkg (already has status $(cat "$d/status"))"; return; }
+  log START "$pkg"; mkdir -p "$d/reviews" "$d/rc"
+  if [ "$PREBUILT" = 0 ]; then
+    bash "$TOOLS/sandbox.sh" "$pkg" --root "$R1" --sb "$SB" >> "$LOG" 2>&1 || { log FAIL "$pkg sandbox"; echo invalid > "$d/status"; return; }
+    bash "$TOOLS/radar-index.sh" "$pkg" --root "$R1" --sb "$SB" >> "$LOG" 2>&1 || { log FAIL "$pkg radar-index"; echo invalid > "$d/status"; return; }
+  fi
+  # reviewers of the panel: rid:role:model:cp1:cp2
+  local -a REV=()
+  while IFS= read -r spec; do REV+=("$spec"); done < <(jq -r --arg p "$PANEL" '.[$p].roles as $r
+    | ($r.searcher|"\(.rid):searcher:\(.model):\(.checkpoints[0]):\(.checkpoints[1])"),
+      ($r.reader|.model as $m|.checkpoints as $c|.rids[]|"\(.):reader:\($m):\($c[0]):\($c[1])")' "$CFG")
+  t0=$(date +%s%3N)
+  dl=$(py "$TOOLS/values.py" deadlines "$PANEL" "$pkg" "$COLLAB" "$t0" --root "$R1") || { log FAIL "$pkg deadlines"; echo invalid > "$d/status"; return; }
+  fin=$(jq -r .FINISH_MS <<<"$dl"); guard=$(jq -r .GUARD_MS <<<"$dl")
+  local roles='{}' models='{}' orders='{}'
+  for spec in "${REV[@]}"; do
+    IFS=: read -r rid role model cp1 cp2 <<<"$spec"; ord=$(order "$rid" "$role")
+    roles=$(jq -c --arg r "$rid" --arg v "$role" '.+{($r):$v}' <<<"$roles"); models=$(jq -c --arg r "$rid" --arg v "$model" '.+{($r):$v}' <<<"$models")
+    orders=$(jq -c --arg r "$rid" --arg v "$ord" '.+{($r):$v}' <<<"$orders")
+  done
+  jq -n -c --arg row "$ROW" --arg pkg "$pkg" --arg panel "$PANEL" --argjson c "$COLLAB" --argjson t0 "$t0" --argjson dl "$dl" \
+    --argjson roles "$roles" --argjson models "$models" --argjson orders "$orders" --arg cs "$(sha "$SB/cand/$pkg/candidate.md")" \
+    '{row:$row,pkg:$pkg,panel:$panel,collab:$c,T0_MS:$t0,FINISH_MS:$dl.FINISH_MS,GUARD_MS:$dl.GUARD_MS,HANG_MS:$dl.HANG_MS,B:$dl.B,
+      values:$dl.values,k:$dl.k,T_report:$dl.T_report,role:$roles,model:$models,order:$orders,cand_sha256:$cs}' > "$d/run.json"
+  if [ "$COLLAB" = 1 ]; then
+    mkdir -p "$d/settings" "$d/board"/{tele,msgs,metrics,snap,state,ctx}  # ctx/: the hook's frozen inputs (radar-hook.sh header)
+    cp "$R1/config/catalogue.json" "$d/board/ctx/catalogue.json"; cp "$R1/index/$pkg.json" "$d/board/ctx/index.json"
+    jq -c --arg p "$PANEL" --arg src "$SB/cand/$pkg/source.md" '.[$p].roles|{searcher:.searcher.rid,readers:.reader.rids,srcpath:$src}' "$CFG" \
+      > "$d/board/ctx/panel.json" || { log FAIL "$pkg board ctx"; echo invalid > "$d/status"; return; }
+    for spec in "${REV[@]}"; do
+      IFS=: read -r rid role model cp1 cp2 <<<"$spec"; k=$(jq -r --arg r "$role" '.k[$r]' "$d/run.json")
+      bash "$TOOLS/settings-gen.sh" "$d/board" "$ROW/$pkg" "$rid" "$role" "$t0" "$fin" "$guard" "$k" "$cp1" "$cp2" "$(order "$rid" "$role")" "$pkg" "" \
+        > "$d/settings/$rid.json" || { log FAIL "$pkg settings-gen $rid"; echo invalid > "$d/status"; return; }
+    done
+  fi
+  for spec in "${REV[@]}"; do
+    IFS=: read -r rid role model cp1 cp2 <<<"$spec"
+    ( bash "$TOOLS/run-reviewer.sh" "$ROW" "$pkg" "$rid" "$model" "$COLLAB" "$t0" --root "$R1" --sb "$SB" >> "$d/reviews/$rid.runner.log" 2>&1; echo $? > "$d/rc/$rid" ) &
+  done
+  wait
+  for spec in "${REV[@]}"; do rid=${spec%%:*}; [ "$(cat "$d/rc/$rid" 2>/dev/null)" = 0 ] || { any_bad=1; log FAIL "$pkg reviewer $rid rc=$(cat "$d/rc/$rid" 2>/dev/null)"; }; done
+  py "$TOOLS/collab_summary.py" pre "$ROW" "$pkg" --root "$R1" --sb "$SB" --a1 "$A1" >> "$d/summary.log" 2>&1; rc=$?
+  [ -f "$d/collab.json" ] && while IFS= read -r a; do log ALARM "$a"; echo "ALARM $a" >&2; done < <(jq -r '.alarms[]?' "$d/collab.json")
+  if [ $rc = 3 ]; then log FAIL "$pkg quarantined: $(cat "$d/QUARANTINED" 2>/dev/null)"; echo quarantined > "$d/status"; return; fi
+  if [ $rc != 0 ]; then log FAIL "$pkg collab_summary pre rc=$rc"; echo invalid > "$d/status"; return; fi
+  if [ $any_bad = 1 ]; then echo invalid > "$d/status"; return; fi
+  local -a RARGS=(); for spec in "${REV[@]}"; do rid=${spec%%:*}; RARGS+=(--report "$rid=$d/reviews/$rid.md"); done
+  jq -c --argjson rev "$(jq -c --slurpfile run "$d/run.json" --arg p "$PANEL" '.[$p].resolution as $res | $run[0].model as $m
+      | [$run[0].role|keys[] | {reviewer_id:., model:$m[.], alias:$res[.].alias, tier:$res[.].tier, strategy:"fixed", stand_in:false,
+          fallback_depth:0, fallbacks:[], launch:null, seed:null, slot_id:(split("-")[0])}]' "$CFG")" \
+    '.reviewers=$rev' "$A1/$pkg/resolution-live7.json" > "$d/resolution.json" || { log FAIL "$pkg resolution"; echo invalid > "$d/status"; return; }
+  superclaude review merge --ledger "$d/ledger.json" --doc "$A1/$pkg/candidate.md" --round 1 "${RARGS[@]}" \
+    --resolution "$d/resolution.json" --out "$d/merged-1.md" > "$d/merge-stdout.txt" 2>&1 || { log FAIL "$pkg merge refused"; echo invalid > "$d/status"; return; }
+  bash "$TOOLS/anon.sh" "$ROW" "$pkg" --root "$R1" >> "$d/summary.log" 2>&1 || { log FAIL "$pkg anon"; echo invalid > "$d/status"; return; }
+  py "$TOOLS/collab_summary.py" post "$ROW" "$pkg" --root "$R1" --sb "$SB" --a1 "$A1" >> "$d/summary.log" 2>&1 || { log FAIL "$pkg collab_summary post"; echo invalid > "$d/status"; return; }
+  n=$(jq -r '.anon_leak // 0' "$d/collab.json")
+  if [ "$n" -gt 0 ]; then echo "anon_leak=$n" > "$d/QUARANTINED"; log FAIL "$pkg quarantined: anon_leak=$n"; echo quarantined > "$d/status"; return; fi
+  local op lab c sc
+  op=$(jq -r .opaque "$d/label-key.json"); lab=$(jq -r .label "$d/label-key.json")
+  c=$(realpath -m --relative-to="$A1/arms/scoring/combos" "$R1/scoring/$op"); sc=$R1/scoring/$op/$pkg/$lab/score.json
+  for n in 1 2; do  # the unchanged judge; it skips when score.json exists, so a second call only follows a failed first one
+    bash "$JUDGE" "$c" "$pkg" "$lab" >> "$d/judge-run.log" 2>&1
+    jq -e . "$sc" >/dev/null 2>&1 && break
+  done
+  if jq -e . "$sc" >/dev/null 2>&1; then echo ok > "$d/status"; log END "$pkg ok"; else echo judge_failed > "$d/status"; log FAIL "$pkg judge_failed"; fi
+}
+for p in "${PKGS[@]}"; do run_package "$p"; done
+
+# ---------------------------------------------------------------- 8. results
+bad=0; for p in "${PKGS[@]}"; do [ "$(cat "$R1/runs/$ROW/$p/status" 2>/dev/null)" = ok ] || bad=1; done
+if out=$(py "$TOOLS/results.py" "$ROW" --root "$R1" --a1 "$A1" 2>&1); then echo "$out"; log END "row $ROW $out"; else echo "$out" >&2; log FAIL "results.py: $out"; bad=1; fi
+bash "$TOOLS/cleanup-sessions.sh" "$ROW" --root "$R1" --sb "$SB" >> "$LOG" 2>&1 || log FAIL "cleanup-sessions"
+exit $bad

Codegraph context: index_state: fresh; checked_at: 2026-11-13T22:17:42Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel. call codegraph only when index_state: fresh, never to widen scope. Q2b dependents not in the diff (Grep floor; shell and markdown files are not indexed): none outside the diff; launch.sh is called only by spikes/spike4.sh and tests/test_launch.py (and the existing tests/test_order.py, whose --order mode is unchanged).
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