# ruff: noqa: N803  (S0, S2, S3 are the design's spike names)
"""launch.sh (DESIGN.md 5.1, 5.2): T-10 gate order, the kill switch (AC-4) and the launch parts of F-4, F-5, F-10, F-11, F-12.

The `claude` and `superclaude` executables are stubs on PATH (never the gateway). The real, unchanged judge-one.sh runs with the
stub judge; it reads ground truth from the real A1DIR (read only) and writes into the tmp root through the relative-path trick.
"""

import json
import os
import shutil
import subprocess

import pytest
from conftest import A1DIR, FIX, R1, REPO, TOOLS, finding, json_reply, report, run

DS = "TASK-WF-designSpec-20261107-075614"

CLAUDE = r"""#!/usr/bin/env bash
D=${STUB_DIR:?}
cat > "$D/stdin.$$"
MODEL=; SETTINGS=
for ((i = 1; i <= $#; i++)); do
  case ${!i} in --model) j=$((i + 1)); MODEL=${!j};; --settings) j=$((i + 1)); SETTINGS=${!j};; esac
done
if [ "$MODEL" = claude-opus-5-5 ]; then  # the blind judge
  n=$(( $(cat "$D/judge.count" 2>/dev/null || echo 0) + 1 )); echo "$n" > "$D/judge.count"
  [ "$n" -le "${STUB_JUDGE_FAILS:-0}" ] && exit 1
  p=$(grep -o 'Write JSON to [^ ]*score.json' "$D/stdin.$$" | head -1 | sed 's/^Write JSON to //')
  cp "$D/score.body" "$p"; printf '[{"type":"result","result":"ok","session_id":"judge"}]\n'; exit 0
fi
if [ -n "${STUB_BAD_BOARD:-}" ] && [ -n "$SETTINGS" ]; then  # a leaking board line: an anchor key is not allowed in panel-msg/1
  board=$(printf '%s' "$SETTINGS" | jq -r '.hooks.PostToolUse[0].hooks[0].command' | grep -o "'[^']*'" | head -1 | tr -d "'")
  printf '{"v":"panel-msg/1","id":"m-x-06","run":"r","from":"radar","to":"t4-1","t":1,"kind":"move","move":"M3","anchor":"x"}\n' >> "$board/msgs/radar.jsonl"
fi
[ -n "${STUB_REVIEWER_EXIT:-}" ] && exit "$STUB_REVIEWER_EXIT"
sed "s/@@MODEL@@/$MODEL/g" "$D/reply"
"""

SUPERCLAUDE = r"""#!/usr/bin/env bash
out=; led=; reps=()
for ((i = 1; i <= $#; i++)); do
  case ${!i} in --out) j=$((i + 1)); out=${!j};; --ledger) j=$((i + 1)); led=${!j};; --report) j=$((i + 1)); reps+=("${!j}");; esac
done
touch "${STUB_DIR:?}/merge.called"
[ -n "${STUB_MERGE_RC:-}" ] && { echo "merge refused: no valid findings block"; exit "$STUB_MERGE_RC"; }
echo '{"rows":[{},{},{}]}' > "$led"
{ echo "verdict: FAIL"; for r in "${reps[@]}"; do echo "report ${r#*=} (${r%%=*})"; done; } > "$out"
"""


class L:
    """A tmp R1 root with one prebuilt fixture sandbox for the DS package, stub executables and a launch() helper."""

    def __init__(self, tmp_path, root):
        self.root, self.tmp = root, tmp_path
        self.sb = tmp_path / "sb"
        repo = self.sb / DS / "repo"
        (repo / "src").mkdir(parents=True)
        (repo / "src" / "a.py").write_text("x\n")
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "s"], cwd=repo, check=True)
        cand = self.sb / "cand" / DS
        cand.mkdir(parents=True)
        shutil.copy(FIX / "cand" / "candidate.md", cand / "candidate.md")
        (cand / "source.md").write_text("# source\n")
        (root / "index").mkdir()
        shutil.copy(FIX / "index.json", root / "index" / f"{DS}.json")
        self.set_gates(S3=False)
        vals = run(["uv", "run", "python", str(TOOLS / "values.py"), "show", "el2", DS, "--root", str(root)]).stdout
        v = root / "values" / "el2" / f"{DS}.json"
        v.parent.mkdir(parents=True)
        v.write_text(vals)
        import hashlib
        (v.parent / f"{DS}.json.sha256").write_text(hashlib.sha256(vals.encode()).hexdigest() + f"  {DS}.json\n")
        self.stub = tmp_path / "stub"
        self.bin = tmp_path / "bin"
        self.stub.mkdir()
        self.bin.mkdir()
        for name, body in (("claude", CLAUDE), ("superclaude", SUPERCLAUDE)):
            (self.bin / name).write_text(body)
            (self.bin / name).chmod(0o755)
        (self.stub / "reply").write_text(json_reply(report(finding())))
        (self.stub / "score.body").write_text(json.dumps({"label": "R", "gt_covered_any": ["GT2"], "gt_covered_blocking": [],
                                                          "ledger_rows_total": 3, "wrong_blockers": 0}))
        home = tmp_path / "home"
        home.mkdir()
        self.env = dict(os.environ, PATH=f"{self.bin}:{os.environ['PATH']}", STUB_DIR=str(self.stub), HOME=str(home))
        self.env.pop("NOFALLBACK", None)
        self.env.pop("PANEL_COLLAB", None)

    def set_gates(self, S0=True, S2=True, S3=True):
        g = {"G-BASE": "pass", "G-PINS": "pass", "S0": "pass" if S0 else "missing", "S2": "pass" if S2 else "missing",
             "S3": "pass" if S3 else "missing", "Spike 4": "pass", "REQ-S3": "recorded"}
        (self.root / "spikes").mkdir(exist_ok=True)
        (self.root / "spikes" / "gate0.json").write_text(json.dumps(g))

    def launch(self, collab=1, rep=0, panel="el2", **env):
        e = dict(self.env, PANEL_COLLAB=str(collab), **{k: str(v) for k, v in env.items()})
        return run(["bash", str(TOOLS / "launch.sh"), "--root", str(self.root), "--sb", str(self.sb), "--prebuilt", panel, str(rep), DS],
                   env=e, timeout=400)

    def d(self, row):
        return self.root / "runs" / row / DS

    def status(self, row):
        return (self.d(row) / "status").read_text().strip()

    def log(self, row):
        return (self.root / "runs" / row / "launch.log").read_text()

    def judge_calls(self):
        p = self.stub / "judge.count"
        return int(p.read_text()) if p.exists() else 0


@pytest.fixture
def lenv(tmp_path, root):
    return L(tmp_path, root)


# ---------------------------------------------------------------- T-10 gate order (AC-2)
def test_gate_order_s3_blocks_only_rep_ge_1(lenv):
    r = lenv.launch(collab=1, rep=1)
    assert r.returncode == 2 and "S3" in r.stderr and not (lenv.root / "runs" / "el2-c1-r1" / "launch.log").exists()
    r = lenv.launch(collab=1, rep=0)  # the smoke row (rep 0) needs only G-BASE, G-PINS, S0, S2 and the values file
    assert r.returncode == 0, r.stdout + r.stderr
    assert "START" in lenv.log("el2-c1-r0") and lenv.status("el2-c1-r0") == "ok"


def test_gate_order_without_s0_refuses_both(lenv):
    lenv.set_gates(S0=False, S3=False)
    for rep in (0, 1):
        r = lenv.launch(collab=1, rep=rep)
        assert r.returncode == 2 and "S0" in r.stderr
    assert lenv.launch(collab=0, rep=0).returncode == 0  # a collab-0 row needs only G-BASE and G-PINS


# ---------------------------------------------------------------- preflight refusals (5.2 step 1)
def test_preflight_refusals(lenv):
    assert lenv.launch(collab=2).returncode == 2
    assert lenv.launch(collab="").returncode == 2  # set-but-empty is not the default: the kill switch must be 0 or 1
    assert lenv.launch(collab=0, NOFALLBACK=0).returncode == 2
    assert lenv.launch(collab=0, NOFALLBACK="").returncode == 2
    shutil.rmtree(lenv.root / "values")
    r = lenv.launch(collab=1, rep=0)
    assert r.returncode == 2 and "Spike 4" in r.stderr
    (lenv.root / "results").mkdir()
    (lenv.root / "results" / "el2-c0-r0.json").write_text("{}")
    assert lenv.launch(collab=0, rep=0).returncode == 2  # a finished row is never re-run
    (lenv.root / "results" / "el2-c0-r0.json").unlink()
    (lenv.root / "config" / "catalogue.json").write_text("{}")
    r = lenv.launch(collab=0, rep=0)
    assert r.returncode == 2 and "catalogue" in r.stderr


# ---------------------------------------------------------------- resume of a partial row (5.2 step 1)
def test_resume_skips_ok_package_and_keeps_other_attempts_aside(lenv):
    d = lenv.d("el2-c0-r0")
    d.mkdir(parents=True)
    (d / "status").write_text("ok\n")
    lenv.launch(collab=0, rep=0)
    assert "SKIP" in lenv.log("el2-c0-r0") and not (d / "reviews").exists() and lenv.judge_calls() == 0
    shutil.rmtree(lenv.root / "runs")
    shutil.rmtree(lenv.root / "results")
    d.mkdir(parents=True)
    (d / "status").write_text("invalid\n")
    (d / "marker").write_text("earlier attempt\n")
    assert lenv.launch(collab=0, rep=0).returncode == 0
    kept = list(d.parent.glob(f"{DS}.prev-*"))
    assert len(kept) == 1 and (kept[0] / "marker").exists() and lenv.status("el2-c0-r0") == "ok"


# ---------------------------------------------------------------- kill switch (AC-4)
def test_collab0_row_has_no_hooks_no_msgs_no_settings(lenv):
    shutil.rmtree(lenv.root / "values")  # no values file yet (Spike 4 itself runs collab-0 rows): planning values, 2.0 x B hang guard
    r = lenv.launch(collab=0, rep=0)
    assert r.returncode == 0, r.stdout + r.stderr
    d = lenv.d("el2-c0-r0")
    assert not (d / "settings").exists() and not (d / "board" / "msgs").exists()
    for m in (d / "reviews").glob("*.meta.json"):
        if ".attempt" in m.name:
            continue
        assert all("--settings" not in a for a in json.loads(m.read_text())["argv"][0])
    run_json = json.loads((d / "run.json").read_text())
    assert run_json["values"] == "planning" and run_json["collab"] == 0
    assert run_json["HANG_MS"] - run_json["T0_MS"] == 232_000  # 2.0 x planning B (116 s)
    row = json.loads((lenv.root / "results" / "el2-c0-r0.json").read_text())
    assert row["status"] == "incomplete" and row["collab_counters"]["injections"] == 0  # a one-package smoke is incomplete by design


# ---------------------------------------------------------------- F-5 hook not firing
def test_f5_hook_not_firing_alarm(lenv):
    r = lenv.launch(collab=1, rep=0)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALARM hook_calls=0 t2b-1" in lenv.log("el2-c1-r0")
    settings = lenv.d("el2-c1-r0") / "settings"
    assert sorted(p.name for p in settings.iterdir()) == ["t2b-1.json", "t3-1.json", "t4-1.json"]
    ctx = lenv.d("el2-c1-r0") / "board" / "ctx"
    assert json.loads((ctx / "panel.json").read_text())["readers"] == ["t4-1", "t3-1"] and (ctx / "index.json").exists()


# ---------------------------------------------------------------- F-10 misroute / binary missing
def test_f10_reviewers_invalid_no_merge_no_fallback(lenv):
    r = lenv.launch(collab=0, rep=0, STUB_REVIEWER_EXIT=127)
    assert r.returncode == 1
    assert lenv.status("el2-c0-r0") == "invalid"
    assert not (lenv.stub / "merge.called").exists() and lenv.judge_calls() == 0
    expected = {"t2b-1": "muse-ember-1.0", "t4-1": "gpt-6-luna", "t3-1": "gpt-6-luna"}
    for rid, model in expected.items():
        meta = json.loads((lenv.d("el2-c0-r0") / "reviews" / f"{rid}.meta.json").read_text())
        assert meta["valid"] is False and meta["attempts"] <= 2
        for argv in meta["argv"]:
            assert argv[argv.index("--model") + 1] == model
    assert not list((lenv.root / "runs").rglob("fallback.log"))


# ---------------------------------------------------------------- F-11 merge refuses
def test_f11_merge_refused_keeps_stdout(lenv):
    r = lenv.launch(collab=0, rep=0, STUB_MERGE_RC=1)
    assert r.returncode == 1 and lenv.status("el2-c0-r0") == "invalid"
    assert "merge refused" in (lenv.d("el2-c0-r0") / "merge-stdout.txt").read_text()
    assert lenv.judge_calls() == 0


# ---------------------------------------------------------------- F-12 judge failure
def test_f12_judge_fails_once_then_succeeds(lenv):
    r = lenv.launch(collab=0, rep=0, STUB_JUDGE_FAILS=1)
    assert r.returncode == 0, r.stdout + r.stderr
    assert lenv.judge_calls() == 2 and lenv.status("el2-c0-r0") == "ok"


def test_f12_judge_always_fails(lenv):
    r = lenv.launch(collab=0, rep=0, STUB_JUDGE_FAILS=9)
    assert r.returncode == 1 and lenv.judge_calls() == 2 and lenv.status("el2-c0-r0") == "judge_failed"
    row = json.loads((lenv.root / "results" / "el2-c0-r0.json").read_text())
    assert row["packages"][DS]["status"] == "judge_failed" and row["status"] == "incomplete"


# ---------------------------------------------------------------- F-4 leak -> quarantine -> no merge, no judge
def test_f4_leaking_board_line_quarantines_package(lenv):
    r = lenv.launch(collab=1, rep=0, STUB_BAD_BOARD=1)
    assert r.returncode == 1
    assert lenv.status("el2-c1-r0") == "quarantined" and (lenv.d("el2-c1-r0") / "QUARANTINED").exists()
    assert not (lenv.stub / "merge.called").exists() and lenv.judge_calls() == 0


def test_launch_order_mode_and_paths_exist():
    assert subprocess.run(["bash", str(TOOLS / "launch.sh"), "--order", "t4-1", "reader"], capture_output=True, text=True).stdout.strip() \
        == "M3,M5,M6,M9,M8,M10"
    assert (A1DIR / "tools" / "tmp-scripts" / "judge-one.sh").exists() and R1.exists() and REPO.exists()
