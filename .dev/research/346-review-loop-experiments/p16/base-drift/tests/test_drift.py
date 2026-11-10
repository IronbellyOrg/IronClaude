"""Offline tests of the base-drift tooling.  Run: cd $SP/p16/base-drift && python3 tests/test_drift.py   (stdlib only; exit 0 = pass)"""
import contextlib
import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import traceback

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import advance  # noqa: E402
import harness as h  # noqa: E402

P11 = h.P11
RV = h.D + "/review/"
TESTS = []


def test(f):
    TESTS.append(f)
    return f


def fresh_env():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="drift-test-", dir=h.SP / "p16"))
    h.RUNS = tmp / "runs"
    h.TASKS_GLOB = str(tmp / "tasks" / "*.output")
    (tmp / "tasks").mkdir()
    return tmp


def run_adv(*a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        advance.main(list(a))
    return buf.getvalue()


def launches(out):
    return [(pathlib.Path(m.group(1)).parent.name, pathlib.Path(m.group(1)).stem.replace("PROMPT-", ""))
            for m in re.finditer(r"^LAUNCH (\S+) model=sonnet$", out, re.M)]


_n = [0]


def fake_worker(tmp, run, step, output_src=None, tokens=(100, 250, 40), model="claude-sonnet-5-5", done=True):
    """Write the step's output file (copied from a p11 report) and a transcript whose first message is the pasted PROMPT text."""
    if output_src is not None:
        dst = h.out_path(run, step)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(output_src, dst)
    prompt = (h.run_dir(run) / f"PROMPT-{step}.md").read_text()
    _n[0] += 1
    lines = [json.dumps({"type": "user", "message": {"role": "user", "content": [{"type": "text", "text": prompt}]}})]
    for i, ot in enumerate(tokens):   # each message id appears twice (one line per content block): counted once at max
        for blk in ({"type": "thinking", "thinking": "x"}, {"type": "tool_use", "name": "Read", "input": {}}):
            lines.append(json.dumps({"type": "assistant", "message": {"id": f"msg_{_n[0]}_{i}", "role": "assistant", "model": model,
                                     "usage": {"output_tokens": ot if blk["type"] == "tool_use" else ot // 2}, "content": [blk]}}))
    if done:
        lines.append(json.dumps({"type": "assistant", "message": {"id": f"msg_{_n[0]}_h", "role": "assistant", "model": model, "usage": {"output_tokens": 5},
                                 "content": [{"type": "tool_use", "name": "SubagentHandback", "input": {"message": f"DONE {h.out_path(run, step)}"}}]}}))
    (tmp / "tasks" / f"a{_n[0]:04d}.output").write_text("\n".join(lines) + "\n")
    return sum(tokens) + (5 if done else 0)


def p11out(run, step):
    if step in ("AUD", "AUD2"):
        return P11 / "runs" / run / "aud/ws" / h.AUD_OUT
    return P11 / "runs" / run / "ws" / h.OUT[step]


@test
def inputs_are_byte_identical_to_p11():
    tmp = fresh_env()
    h.build()
    for run in h.RUN_NAMES:
        assert h.sha(h.run_dir(run) / "command.md") == h.CMD_SHA == h.sha(P11 / "runs/a3-r1/command.md")
        rp = "home/.claude/rules/prompts/document_review_loop_prompts.md"
        assert h.sha(h.run_dir(run) / rp) == h.RULES_SHA == h.sha(P11 / "rules.md")
        assert h.sha(h.ws(run) / h.SPEC) == h.SPEC_SHA
        # whole sandbox tree equals a p11 arm-3 sandbox (same file list and hashes), ignoring state/prompt files
        def tree(base):
            return {str(p.relative_to(base)): h.sha(p) for p in sorted(base.rglob("*")) if p.is_file() and p.name not in ("state.json",)
                    and not p.name.startswith("PROMPT-") and "/ws/.dev/orca-command-refactor/review/" not in str(p) and "/specs/history/" not in str(p) and p.name != "orca-worker-contract-spec.md"}
        a, b = tree(h.run_dir(run)), tree(P11 / "runs/a3-r1")
        b = {k: v for k, v in b.items() if not k.startswith("aud/")}
        assert a == b, set(a) ^ set(b)
    shutil.rmtree(tmp)


@test
def briefs_equal_p11_modulo_paths():
    tmp = fresh_env()
    h.build()
    run, base = "a3d-r1", "a3-r1"

    def swap(t, sub=""):
        return t.replace(str(P11 / "runs" / base), str(h.run_dir(run)))
    for step in ("R1", "R2"):
        h.prep(run, step) if True else None
        mine = (h.run_dir(run) / f"PROMPT-{step}.md").read_text()
        theirs = swap((P11 / "runs" / base / f"PROMPT-{step}.md").read_text())
        assert mine == theirs, step
    ids = re.search(r"IDS=(.*?)\.\nInputs:", (P11 / "runs" / base / "PROMPT-V1.md").read_text(), re.S).group(1)
    shutil.copy(p11out(base, "R1"), h.out_path(run, "R1"))
    h.prep(run, "V1", {"IDS": ids})
    assert (h.run_dir(run) / "PROMPT-V1.md").read_text() == swap((P11 / "runs" / base / "PROMPT-V1.md").read_text())
    # auto-parsed IDS for the same R1 report equal what p11 pasted
    assert h.ids_from(h.out_path(run, "R1")) == ids, (h.ids_from(h.out_path(run, "R1")), ids)
    # audit prompts: same text as p11 AUD, with aud / aud2 sandboxes
    h.prep(run, "AUD")
    assert (h.run_dir(run) / "PROMPT-AUD.md").read_text() == swap((P11 / "runs" / base / "PROMPT-AUD.md").read_text())
    h.prep(run, "AUD2")
    a2 = (h.run_dir(run) / "PROMPT-AUD2.md").read_text()
    assert a2 == swap((P11 / "runs" / base / "PROMPT-AUD.md").read_text()).replace(f"{run}/aud", f"{run}/aud2")
    # aud sandboxes: command, rules, overlay, spec equal the baseline audit sandbox
    for sub in ("aud", "aud2"):
        d = h.run_dir(run) / sub
        assert h.sha(d / "command.md") == h.CMD_SHA and h.sha(d / "ws" / h.SPEC) == h.SPEC_SHA
        assert h.sha(d / "home/.claude/rules/prompts/document_review_loop_prompts.md") == h.RULES_SHA
        assert (d / "ws" / h.D / "review").is_dir() and not any((d / "ws" / h.D / "review").iterdir())
    shutil.rmtree(tmp)


@test
def dry_run_marks_nothing():
    tmp = fresh_env()
    out = run_adv("--dry-run")
    assert sorted(launches(out)) == [("a3d-r1", "R1"), ("a3d-r2", "R1")], out
    for run in h.all_runs():
        st = h.load(run)
        assert st["launched"] == {} and st["done"] == []
        assert (h.run_dir(run) / "PROMPT-R1.md").exists()
    # a real call launches, marks, then a second call relaunches nothing
    out = run_adv()
    assert len(launches(out)) == 2 and "RUNNING 2" in out
    out2 = run_adv()
    assert launches(out2) == [] and "RUNNING 2" in out2
    shutil.rmtree(tmp)


@test
def full_loop_r1_fail_r2_pass_and_token_accounting():
    tmp = fresh_env()
    run_adv()
    exp = {}
    for run, base in (("a3d-r1", "a3-r1"), ("a3d-r2", "a3-r2")):
        exp[run] = fake_worker(tmp, run, "R1", p11out(base, "R1"), tokens=(100, 250, 40))
    out = run_adv()
    assert sorted(launches(out)) == [("a3d-r1", "V1"), ("a3d-r2", "V1")], out
    for run, base in (("a3d-r1", "a3-r1"), ("a3d-r2", "a3-r2")):
        assert h.load(run)["log"]["R1"]["output_tokens"] == exp[run] == 395, (exp[run], "message ids counted once at max output_tokens")
        exp[run] += fake_worker(tmp, run, "V1", p11out(base, "V1"), tokens=(7, 9))
    out = run_adv()
    assert sorted(launches(out)) == [("a3d-r1", "R2"), ("a3d-r2", "R2")], out
    for run, base in (("a3d-r1", "a3-r1"), ("a3d-r2", "a3-r2")):
        src = p11out(base, "R2")
        exp[run] += fake_worker(tmp, run, "R2", src, tokens=(30,))
        assert h.load(run)["log"].get("R2") is None
    out = run_adv()
    st = {r: h.load(r) for r in h.all_runs()}
    for r in h.all_runs():
        assert st[r]["log"]["R2"]["verdict"] == "PASS", r
        assert st[r]["loop_end"] == "PASS"
    # both audits of each run launch together
    assert sorted(launches(out)) == [("a3d-r1", "AUD"), ("a3d-r1", "AUD2"), ("a3d-r2", "AUD"), ("a3d-r2", "AUD2")], out
    for run, base in (("a3d-r1", "a3-r1"), ("a3d-r2", "a3-r2")):
        assert (h.run_dir(run) / "aud/ws" / h.SPEC).exists() and (h.run_dir(run) / "aud2/ws" / h.SPEC).exists()
        fake_worker(tmp, run, "AUD", p11out(base, "AUD"), tokens=(50, 60))
        fake_worker(tmp, run, "AUD2", p11out(base, "AUD"), tokens=(70, 80))
    out = run_adv()
    assert "ALL DONE" in out, out
    for r in h.all_runs():
        s = h.load(r)
        assert s["complete"] and s["log"]["AUD"]["output_tokens"] == 115 and s["log"]["AUD2"]["output_tokens"] == 155
        assert sum(s["log"].get(x, {}).get("output_tokens", 0) for x in h.LOOP_STEPS) == exp[r]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        h.analyze()
    txt = buf.getvalue()
    assert "a3d-r1" in txt and "fresh loop mean" in txt and "ratio" in txt, txt
    shutil.rmtree(tmp)


@test
def r3_path_and_failure_handling():
    tmp = fresh_env()
    run = "a3d-r1"
    run_adv()
    base = "a3-r6"   # p11 run that needed V1 R2 V2 R3
    fake_worker(tmp, run, "R1", p11out(base, "R1"))
    run_adv()
    fake_worker(tmp, run, "V1", p11out(base, "V1"))
    run_adv()
    fake_worker(tmp, run, "R2", p11out(base, "R2"))
    out = run_adv()
    assert ("a3d-r1", "V2") in launches(out), out
    fake_worker(tmp, run, "V2", p11out(base, "V2"))
    out = run_adv()
    assert ("a3d-r1", "R3") in launches(out)
    fake_worker(tmp, run, "R3", p11out(base, "R3"))
    out = run_adv()
    assert ("a3d-r1", "AUD") in launches(out) and ("a3d-r1", "AUD2") in launches(out), out
    assert h.load(run)["loop_end"] in ("PASS", "R3-FAIL")
    # a worker that returns without its output file is relaunched once, then the run is LOST
    run2 = "a3d-r2"
    fake_worker(tmp, run2, "R1", None)
    out = run_adv()
    assert "MANUAL a3d-r2 R1" in out and ("a3d-r2", "R1") in launches(out), out
    assert h.load(run2)["relaunch"]["R1"] == 1
    for f in (tmp / "tasks").glob("*.output"):
        f.unlink()
    fake_worker(tmp, run2, "R1", None)
    out = run_adv()
    assert "LOST a3d-r2 R1" in out and h.load(run2)["lost"], out
    shutil.rmtree(tmp)


@test
def token_matching_is_by_prompt_text_and_model():
    tmp = fresh_env()
    run_adv()
    fake_worker(tmp, "a3d-r1", "R1", None, tokens=(11, 22), model="claude-haiku-4-5", done=True)   # wrong model -> ignored
    fake_worker(tmp, "a3d-r2", "R1", None, tokens=(5, 6))
    idx = h.scan_transcripts()
    assert set(idx) == {("a3d-r1", "R1"), ("a3d-r2", "R1")}
    assert h.pick(idx[("a3d-r1", "R1")], "sonnet") is None
    assert h.pick(idx[("a3d-r2", "R1")], "sonnet")["tokens"] == 16
    shutil.rmtree(tmp)


@test
def drive_sh_integration():
    """drive.sh prints LAUNCH lines (repo-relative) for the real scratchpad layout; run on a throw-away copy, not on the real dir."""
    probe = h.SP / "p16/_drive_probe"
    if probe.exists():
        shutil.rmtree(probe)
    probe.mkdir(parents=True)
    for f in ("harness.py", "advance.py"):
        shutil.copy(HERE / f, probe / f)
    try:
        out = subprocess.run(["bash", str(h.SP / "drive.sh"), "p16/_drive_probe"], capture_output=True, text=True, timeout=300).stdout
        ls = [ln for ln in out.splitlines() if ln.startswith("LAUNCH")]
        assert len(ls) == 2 and all("p16/_drive_probe/runs/a3d-r" in ln and ln.endswith("model=sonnet") for ln in ls), out
        assert "RUNNING 2" in out, out
    finally:
        shutil.rmtree(probe, ignore_errors=True)


if __name__ == "__main__":
    real = (h.RUNS, h.TASKS_GLOB)
    fails = 0
    for t in TESTS:
        h.RUNS, h.TASKS_GLOB = real
        try:
            t()
            print("PASS", t.__name__)
        except Exception:
            fails += 1
            print("FAIL", t.__name__)
            traceback.print_exc()
    h.RUNS, h.TASKS_GLOB = real
    for d in (h.SP / "p16").glob("drift-test-*"):
        shutil.rmtree(d, ignore_errors=True)
    print(f"{len(TESTS) - fails}/{len(TESTS)} passed")
    sys.exit(1 if fails else 0)
