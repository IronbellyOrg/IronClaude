"""PN2 harness tests. Run: cd $AB && uv run --no-project --with pytest pytest tests

The harness reads PN2_AB (experiment root), PN2_TASKS_GLOB (transcripts) and PN2_PRODUCT_REF, so every test works in a
temporary experiment root and never touches $AB/runs. The lint step uses the real clone (uv run --project)."""
import json, os, pathlib, re, shutil, subprocess, sys
import pytest

AB = pathlib.Path(__file__).resolve().parents[1]
SP = AB.parents[1]
P11 = SP/"p11"
BASE_REF = "69ac8b3335564fb5551980e984c5d9b763039cc1"
sys.path.insert(0, str(AB))
import analysis  # noqa: E402

D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"


def make_root(tmp_path):
    root = tmp_path/"ab2"; root.mkdir()
    shutil.copy(AB/"decision.toml", root/"decision.toml")
    tasks = tmp_path/"tasks"; tasks.mkdir()
    env = dict(os.environ, PN2_AB=str(root), PN2_TASKS_GLOB=str(tasks/"*.output"), PN2_PRODUCT_REF=BASE_REF)
    return root, tasks, env


def hz(env, *args):
    r = subprocess.run([sys.executable, str(AB/"harness.py"), *args], capture_output=True, text=True, env=env, cwd=AB)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


def adv(env, *args):
    r = subprocess.run([sys.executable, str(AB/"advance.py"), *args], capture_output=True, text=True, env=env, cwd=AB)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("pn2")
    root, tasks, env = make_root(tmp)
    hz(env, "build", "sonnet")
    return root, tasks, env


def norm(text, sandbox):
    return text.replace(str(sandbox), "<SB>")


def strip_lint(text):
    return re.sub(r", lint=\.dev/orca-command-refactor/review/lint-\d\.md\.", ".", text).replace(
        ", lint=" + f"{D}/review/lint-1.md.", ".")


# (1) prompt identity ----------------------------------------------------------------------------------------------
def test_r1_prompt_identical_to_stage2_arm3_except_the_lint_value(built):
    root, _, env = built
    ours = (root/"runs/l2-r1/PROMPT-R1.md").read_text()
    ref = (P11/"runs/a3-r1/PROMPT-R1.md").read_text()
    assert f"lint={D}/review/lint-1.md" in ours
    assert norm(strip_lint(ours), root/"runs/l2-r1") == norm(ref, P11/"runs/a3-r1")


def test_v1_r2_r3_aud_prompts_identical(built):
    root, _, env = built
    # V1 for the ids F1, F2 (a3-r1), then R2 (a3-r1), R3 (a3-r6 reference), AUD (a3-r1)
    hz(env, "prep", "l2-r1", "V1", "IDS=F1, F2")
    hz(env, "prep", "l2-r1", "R2")
    for step in ("V1", "R2"):
        ours = (root/f"runs/l2-r1/PROMPT-{step}.md").read_text()
        ref = (P11/f"runs/a3-r1/PROMPT-{step}.md").read_text()
        assert norm(strip_lint(ours), root/"runs/l2-r1") == norm(ref, P11/"runs/a3-r1"), step
    hz(env, "prep", "l2-r6", "V1", "IDS=F1, F2")
    hz(env, "prep", "l2-r6", "R2"); hz(env, "prep", "l2-r6", "V2", "IDS=F1, F2"); hz(env, "prep", "l2-r6", "R3")
    ours = (root/"runs/l2-r6/PROMPT-R3.md").read_text()
    ref = (P11/"runs/a3-r6/PROMPT-R3.md").read_text()
    assert "lint=" + f"{D}/review/lint-3.md" in ours
    assert norm(strip_lint(ours).replace(f", lint={D}/review/lint-3.md.", "."), root/"runs/l2-r6") == norm(ref, P11/"runs/a3-r6")


def test_aud_and_aud2_prompts_equal_the_frozen_audit_prompt(built):
    root, _, env = built
    hz(env, "prep", "l2-r2", "AUD"); hz(env, "prep", "l2-r2", "AUD2")
    ref = norm((P11/"runs/a3-r1/PROMPT-AUD.md").read_text(), P11/"runs/a3-r1/aud")
    a = norm((root/"runs/l2-r2/PROMPT-AUD.md").read_text(), root/"runs/l2-r2/aud")
    b = norm((root/"runs/l2-r2/PROMPT-AUD2.md").read_text(), root/"runs/l2-r2/aud2")
    assert a == ref and b == ref
    assert "lint" not in a.lower().replace("deadline", "")  # the audit gets no lint
    cmd = (root/"runs/l2-r2/aud/command.md").read_bytes()
    import hashlib
    assert hashlib.sha256(cmd).hexdigest() == "e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494"
    rules = (root/"runs/l2-r2/aud/home/.claude/rules/prompts/document_review_loop_prompts.md").read_bytes()
    assert hashlib.sha256(rules).hexdigest() == "3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8"


# (2) token baseline --------------------------------------------------------------------------------------------------
EXPECTED_LOOP = {"a3-r1": 70694, "a3-r2": 109207, "a3-r3": 95213, "a3-r4": 81415, "a3-r5": 94998, "a3-r6": 151017}


def test_basetokens_reproduces_arm3_loop_totals():
    base = analysis.baseline_tokens()
    if len(base) < 6:
        pytest.skip("p11 transcripts not on disk")
    for run, want in EXPECTED_LOOP.items():
        assert abs(base[run]["loop"] - want) / want <= 0.01, (run, base[run]["loop"], want)
    a = sum(v["loop"] for v in base.values()) / 6
    assert abs(a - 100424) / 100424 <= 0.01


# (3) lint step ---------------------------------------------------------------------------------------------------------
def test_lint_step_writes_lint1_with_the_expected_first_line_and_only_live_checks(built):
    root, _, env = built
    p = root/"runs/l2-r3/ws"/D/"review/lint-1.md"
    text = p.read_text()
    first = text.splitlines()[0]
    sha = __import__("hashlib").sha256((root/"runs/l2-r3/ws"/SPEC).read_bytes()).hexdigest()
    assert first == f"lint: superclaude review lint, review-lint/1, sha256 {sha}"
    assert "Checks: REF." in text
    st = json.load(open(root/"runs/l2-r3/state.json"))
    assert st["log"]["LINT1"]["findings"] == len(re.findall(r"(?m)^### LINT-", text))
    assert st["log"]["LINT1"]["checks"] == "REF" and len(st["log"]["LINT1"]["sha256"]) == 64


def test_lint_step_runs_again_before_r2_on_the_revised_candidate(built):
    root, _, env = built
    ws = root/"runs/l2-r4/ws"
    spec = ws/SPEC
    spec.write_text(spec.read_text() + "\nSee also WC-99 for the details, and PH-3 and section 99.1.\n")
    hz(env, "prep", "l2-r4", "V1", "IDS=F1")
    hz(env, "prep", "l2-r4", "R2")
    text = (ws/D/"review/lint-2.md").read_text()
    assert "### LINT-REF-1" in text and "WC-99" in text
    assert not re.search(r"### LINT-(COUNT|KV|PHASE|PATH)", text)
    prompt = (root/"runs/l2-r4/PROMPT-R2.md").read_text()
    assert f"prior={D}/review/round1.md, lint={D}/review/lint-2.md." in prompt
    st = json.load(open(root/"runs/l2-r4/state.json"))
    assert st["log"]["LINT2"]["findings"] >= 1


# (4) happy path with fakes ----------------------------------------------------------------------------------------------
def fake_transcript(tasks, prompt, model="claude-sonnet-5-5", tokens=1000, name=None, done=True):
    lines = [json.dumps({"type": "user", "message": {"role": "user", "content": f"Read {prompt} and follow it exactly."}})]
    lines.append(json.dumps({"message": {"role": "assistant", "id": "m1", "model": model, "usage": {"output_tokens": tokens // 2},
                                          "content": [{"type": "text", "text": "x"}]}}))
    lines.append(json.dumps({"message": {"role": "assistant", "id": "m1", "model": model, "usage": {"output_tokens": tokens},
                                          "content": [{"type": "tool_use", "name": "SubagentHandback" if done else "Read", "input": {"message": "DONE x"}}]}}))
    (tasks/(name or f"w{abs(hash(prompt))}.output")).write_text("\n".join(lines))


def copy_report(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy(src, dst)


def test_happy_path_r1_fail_v1_lint2_r2_pass_then_both_audits_together(tmp_path):
    root, tasks, env = make_root(tmp_path)
    hz(env, "build", "sonnet")
    out = adv(env)
    assert out.count("LAUNCH sonnet") == 6
    for i in range(2, 7): shutil.rmtree(root/"runs"/f"l2-r{i}")   # keep one run so the six slots are free for the pair
    run = "l2-r1"; r = root/"runs"/run; src = P11/"runs/a3-r1"
    copy_report(src/"ws"/D/"review/round1.md", r/"ws"/D/"review/round1.md")
    fake_transcript(tasks, r/"PROMPT-R1.md")
    out = adv(env)
    assert f"[{run}] R1 done: verdict=FAIL" in out
    assert f"LAUNCH sonnet {r}/PROMPT-V1.md" in out
    copy_report(src/"ws"/D/"review/revise1.md", r/"ws"/D/"review/revise1.md")
    fake_transcript(tasks, r/"PROMPT-V1.md")
    out = adv(env)
    assert f"[{run}] V1 done" in out and f"LAUNCH sonnet {r}/PROMPT-R2.md" in out
    st = json.load(open(r/"state.json"))
    assert "LINT2" in st["log"], "lint ran before R2"
    copy_report(src/"ws"/D/"review/round2.md", r/"ws"/D/"review/round2.md")
    fake_transcript(tasks, r/"PROMPT-R2.md")
    out = adv(env)
    assert f"[{run}] R2 done: verdict=PASS" in out
    assert f"LAUNCH sonnet {r}/PROMPT-AUD.md" in out and f"LAUNCH sonnet {r}/PROMPT-AUD2.md" in out
    st = json.load(open(r/"state.json"))
    assert st["stratum"] == "sonnet" and st["log"]["R2"]["stratum"] == "sonnet"


def test_audit_pair_waits_until_two_slots_are_free(tmp_path):
    root, tasks, env = make_root(tmp_path)
    hz(env, "build", "sonnet")
    adv(env)                                             # six R1 launched, six running
    src = P11/"runs/a3-r1"
    r1 = root/"runs/l2-r1"; r2 = root/"runs/l2-r2"
    copy_report(src/"ws"/D/"review/round2.md", r1/"ws"/D/"review/round1.md")   # a PASS report as R1 of l2-r1
    fake_transcript(tasks, r1/"PROMPT-R1.md")
    out = adv(env)
    assert "R1 done: verdict=PASS" in out
    assert "LAUNCH" not in out, "one slot is free, the audit pair needs two"
    copy_report(src/"ws"/D/"review/round1.md", r2/"ws"/D/"review/round1.md")
    fake_transcript(tasks, r2/"PROMPT-R1.md")
    out = adv(env)
    assert f"LAUNCH sonnet {r1}/PROMPT-AUD.md" in out and f"LAUNCH sonnet {r1}/PROMPT-AUD2.md" in out
    assert "PROMPT-V1.md" not in out.split("LAUNCH")[-1] or out.count("LAUNCH") == 2


# (5) concurrency --------------------------------------------------------------------------------------------------------
def test_six_fresh_runs_print_six_launch_lines_and_dry_run_records_nothing(tmp_path):
    root, tasks, env = make_root(tmp_path)
    hz(env, "build", "sonnet")
    before = {p.name: p.read_text() for p in (root/"runs").glob("*/state.json")}
    dry = adv(env, "--dry-run")
    assert dry.count("LAUNCH sonnet") == 6
    assert not (root/"launch-ledger.jsonl").exists()
    assert before == {p.name: p.read_text() for p in (root/"runs").glob("*/state.json")}
    real = adv(env)
    assert real.count("LAUNCH sonnet") == 6
    assert len((root/"launch-ledger.jsonl").read_text().splitlines()) == 6
    again = adv(env)
    assert "LAUNCH" not in again, "already launched prompts are not printed again"


def test_never_more_than_six_running_across_strata(tmp_path):
    root, tasks, env = make_root(tmp_path)
    hz(env, "build", "sonnet"); hz(env, "build", "haiku")
    out = adv(env)
    assert out.count("LAUNCH") == 6 and "LAUNCH haiku" not in out, "six slots are taken by the sonnet runs"


def test_haiku_stratum_loop_workers_haiku_audits_sonnet(tmp_path):
    root, tasks, env = make_root(tmp_path)
    hz(env, "build", "haiku")
    out = adv(env)
    assert out.count("LAUNCH haiku") == 4
    st = json.load(open(root/"runs/l2h-r1/state.json"))
    assert st["stratum"] == "haiku"
    sys.path.insert(0, str(AB));
    env_backup = dict(os.environ); os.environ.update(env)
    try:
        import importlib, harness
        importlib.reload(harness)
        assert harness.model_for("l2h-r1", "R1") == "haiku" and harness.model_for("l2h-r1", "V1") == "haiku"
        assert harness.model_for("l2h-r1", "AUD") == "sonnet" and harness.model_for("l2h-r1", "AUD2") == "sonnet"
        assert harness.model_for("l2-r1", "R1") == "sonnet"
    finally:
        os.environ.clear(); os.environ.update(env_backup)


def test_lost_prompt_is_relaunched_once_then_marked_lost(tmp_path):
    root, tasks, env = make_root(tmp_path)
    hz(env, "build", "sonnet")
    adv(env)
    ledger = root/"launch-ledger.jsonl"
    old = [json.loads(l) for l in ledger.read_text().splitlines()]
    for e in old: e["ts"] -= 3600
    ledger.write_text("\n".join(json.dumps(e) for e in old) + "\n")
    out = adv(env)
    assert out.count("RELAUNCH") == 6
    old = [json.loads(l) for l in ledger.read_text().splitlines()]
    for e in old: e["ts"] -= 3600
    ledger.write_text("\n".join(json.dumps(e) for e in old) + "\n")
    out = adv(env)
    assert out.count("LOST") == 6


# (6) analysis: D1, D2, D3, D4, D6 --------------------------------------------------------------------------------------
CFG = analysis.config()


def test_d6_converted_limits_are_the_stored_constants():
    assert analysis.convert_limit(1.8, CFG) == 2.35
    assert analysis.convert_limit(2.0, CFG) == 2.69
    assert analysis.convert_limit(1.5, CFG) == 1.84
    assert analysis.convert_limit(1.65, CFG) == 2.10
    assert analysis.convert_limit(1.25, CFG) == CFG["drop"]["r_loop_above"] == 1.42
    assert analysis.convert_limit(1.15, CFG) == CFG["adopt"]["r_loop_at_most"] == 1.25


def test_d1_thresholds_unchanged():
    assert CFG["baseline"]["b_blk"] == 1.50 and CFG["drop"]["blk_t_at_least"] == 1.50
    assert CFG["adopt"]["blk_t_drop"] == 0.5 and CFG["adopt"]["theme_ratio_at_most"] == 0.5
    assert abs(CFG["drop"]["pass_t_below"] - 5 / 6) < 1e-6 and CFG["drop"]["growth_above_pct"] == 2.82
    assert CFG["validity"]["aud_gap_max"] == 0.75 and CFG["validity"]["min_completed"] == 5


def test_d2_tokens_dedupe_message_ids_and_loop_only_convention():
    lines = []
    for mid, toks in (("a", 10), ("a", 40), ("b", 25), ("a", 40)):
        lines.append(json.dumps({"message": {"role": "assistant", "id": mid, "usage": {"output_tokens": toks}}}))
    total, done, _ = analysis.transcript_usage(lines)
    assert total == 65 and not done
    b = CFG["baseline"]
    assert b["a_base"] + b["audit_base"] == b["b_base"] == 169468
    m = {"n_completed": 6, "n_planned": 6, "BLK_T": 0.8, "AUD_mean": 0.8, "AUD2_mean": 0.8, "PASS_T": 1.0, "GROWTH_T": 1.5,
         "R_LOOP": 1.0, "THEME_T": 0.2, "THEME_B": 0.8}
    recs = [{"completed": True, "pass": True, "growth_pct": 1.0, "loop_tokens": 100000, "one_audit_tokens": 70000, "r1_tokens": 50000,
             "audits": [{"blocking": 1, "themes": ["T1"]}, {"blocking": 0, "themes": []}]} for _ in range(6)]
    s = analysis.summarize(recs, CFG, 0.8)
    assert abs(s["R_LOOP"] - 100000 / 100424) < 1e-9 and abs(s["R_B"] - 170000 / 169468) < 1e-9
    assert s["R_LOOP"] != s["R_B"], "loop-only A decides; B is reported alongside"


def test_decision_zones():
    base = {"n_completed": 6, "n_planned": 6, "AUD_mean": 1.0, "AUD2_mean": 1.0, "PASS_T": 1.0, "GROWTH_T": 1.5, "THEME_T": 0.2, "THEME_B": 0.8,
            "BLK_T": 0.9, "R_LOOP": 1.0}
    assert analysis.decide(base, CFG)[0] == "ADOPT"
    assert analysis.decide(dict(base, BLK_T=1.5), CFG)[0] == "DROP"
    assert analysis.decide(dict(base, R_LOOP=1.43), CFG)[0] == "DROP"       # post-hoc cost clause at 1.42
    assert analysis.decide(dict(base, R_LOOP=1.40), CFG)[0] == "INCONCLUSIVE"  # inside the band: not <= 1.25, not > 1.42
    assert analysis.decide(dict(base, PASS_T=4 / 6), CFG)[0] == "DROP"
    assert analysis.decide(dict(base, GROWTH_T=2.9), CFG)[0] == "DROP"
    assert analysis.decide(dict(base, BLK_T=1.2), CFG)[0] == "INCONCLUSIVE"
    v, _, band = analysis.decide(dict(base, n_completed=4), CFG)
    assert v == "INCONCLUSIVE" and band is False, "too few runs is a validity problem, not a noise band"
    v, _, band = analysis.decide(dict(base, AUD2_mean=2.0), CFG)
    assert v == "INCONCLUSIVE" and band is False


def test_d3_haiku_pending_and_direction(tmp_path):
    assert analysis.final_verdict("ADOPT", {"status": "pending"}) == "ADOPT (Haiku robustness pending)"
    assert analysis.final_verdict("ADOPT", {"status": "ok"}) == "ADOPT"
    assert analysis.final_verdict("ADOPT", {"status": "against"}).startswith("INCONCLUSIVE")
    assert analysis.final_verdict("DROP", {"status": "ok"}) == "DROP"
    recs = [{"completed": True, "audits": [{"blocking": 1}, {"blocking": 1}]} for _ in range(4)]
    base = tmp_path/"results.json"
    base.write_text(json.dumps({"runs": {f"h{i}": {"audit_blocking": [2, 2]} for i in range(6)}}))
    h = analysis.haiku_check(recs, base)
    assert h["status"] == "ok" and abs(h["relative_reduction"] - 0.5) < 1e-9
    worse = [{"completed": True, "audits": [{"blocking": 3}, {"blocking": 3}]} for _ in range(4)]
    assert analysis.haiku_check(worse, base)["status"] == "against"
    assert analysis.haiku_check(recs, tmp_path/"missing.json")["status"] == "pending"
    inflated = recs[:2] + [{"completed": False, "audits": []}, {"completed": False, "audits": []}]
    assert analysis.haiku_check(inflated, base)["status"] == "against", "harness-failure rate 0.5 against a baseline of 0"


def test_d4_extension_only_from_the_band_and_only_once(tmp_path):
    root, tasks, env = make_root(tmp_path)
    hz(env, "build", "sonnet")
    out = hz(env, "extend")
    assert sorted(p.name for p in (root/"runs").iterdir()) == [f"l2-r{i}" for i in range(1, 10)]
    r = subprocess.run([sys.executable, str(AB/"harness.py"), "extend"], capture_output=True, text=True, env=env, cwd=AB)
    assert r.returncode != 0 and "extension already used" in (r.stdout + r.stderr)


def test_d6_no_gate_in_the_launch_tooling_reads_tokens():
    for name in ("advance.py", "harness.py"):
        src = (AB/name).read_text()
        code = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
        code = re.sub(r'""".*?"""', "", code, flags=re.S)
        assert not re.search(r"R_LOOP|r_loop|output_tokens|loop_tokens|usage\b|abort|kill", code), name
    # cost enters only analysis.decide, which is called after runs completed
    assert "r_loop_above" in (AB/"analysis.py").read_text()


def test_run_records_carry_the_stratum_tag(tmp_path):
    root, tasks, env = make_root(tmp_path)
    hz(env, "build", "haiku"); hz(env, "build", "sonnet")
    for run, want in (("l2h-r1", "haiku"), ("l2-r1", "sonnet")):
        assert json.load(open(root/"runs"/run/"state.json"))["stratum"] == want
    assert "haiku" in hz(env, "status")
