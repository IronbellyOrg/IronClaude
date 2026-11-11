"""Offline tests of the ab4 tooling. No pytest needed (plain asserts):
  cd $AB4 && python3 tests/test_ab4.py          (pytest also collects the test_* functions if it is installed)
Fixtures in tests/fixtures are real reports copied from p12/ab1 runs (banner sections, anomalous id formats, a multi-row verify reply)."""
import contextlib
import glob
import io
import json
import os
import pathlib
import re
import shutil
import sys
import tempfile
import time
import traceback

AB = pathlib.Path(__file__).resolve().parents[1]
FX = AB / "tests" / "fixtures"
sys.path.insert(0, str(AB))
import advance  # noqa: E402
import harness as h  # noqa: E402
import reqlint as L  # noqa: E402
import score_themes as sc  # noqa: E402

RV = ".dev/orca-command-refactor/review/"


@contextlib.contextmanager
def env():
    """Private AB dir (decision.json + frozen/ copied), private RUNS, no transcripts."""
    tmp = pathlib.Path(tempfile.mkdtemp())
    shutil.copy(AB / "decision.json", tmp / "decision.json")
    shutil.copytree(AB / "frozen", tmp / "frozen")
    saved = (h.AB, h.RUNS, h.FROZEN, h.TASKS_GLOB)
    h.AB, h.RUNS, h.FROZEN = tmp, tmp / "runs", tmp / "frozen"
    h.TASKS_GLOB = str(tmp / "none" / "*.output")
    try:
        yield tmp
    finally:
        h.AB, h.RUNS, h.FROZEN, h.TASKS_GLOB = saved
        shutil.rmtree(tmp, ignore_errors=True)


def fx(name): return FX / name


def fail_fixtures():
    out = []
    for f in sorted(FX.glob("*.md")):
        if "verify" in f.name:
            continue
        if sc.verdict_of(f.read_text(errors="ignore")) == "FAIL":
            out.append(f)
    return out


def adv(argv=()):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        advance.main(list(argv))
    return buf.getvalue()


def launches(out): return [ln for ln in out.splitlines() if ln.startswith("LAUNCH ")]


def old_age(p):
    t = time.time() - 600
    os.utime(p, (t, t))


def fake(run, step, text):
    p = h.out_path(run, step)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    old_age(p)
    return p


def verify_reply(ids, confirmed, bad_first_row=None):
    lines = ["| id | found | exists | follows | verdict | reason |", "|---|---|---|---|---|---|"]
    for fid in ids:
        lines.append(f"| {fid} | text | yes | yes | {'confirm' if fid in confirmed else 'reject'} | because |")
    lines.append("confirmed: " + (", ".join(confirmed) if confirmed else "none"))
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ 4(c): ids_from
def test_ids_reviser_brief_banner_form():
    # b1h-r3 R1a ended with "=== REVISER BRIEF ===\n\nBlocking findings: B1, ..., B7." (ab1 needed setids)
    f = fx("b1h-r3__round1-a.md")
    assert sc.parse_ids(sc.ids_from(f)) == ["B1", "B2", "B3", "B4", "B5", "B6", "B7"]


def test_ids_blocking_inline_lists():
    # b1h-r3 R1c: "- Blocking: F1, F2, F3, F4 (four open blocking findings)." and a prose "Reviser brief (blocking finding ids only; ...): revise ..." line
    f = fx("b1h-r3__round1-c.md")
    assert sc.parse_ids(sc.ids_from(f)) == ["F1", "F2", "F3", "F4"]
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "r.md"
        p.write_text("review: 1 of 3\n\n### B1 x\n\ntext\n\nBlocking findings: B1, B2\n\nverdict: FAIL\n")
        assert sc.parse_ids(sc.ids_from(p)) == ["B1", "B2"]
        p.write_text("review: 1 of 3\n\n=== REVISER BRIEF ===\n\nBlocking findings: B3, B4.\n\nRestated bullet 6 ... F9\n\nverdict: FAIL\n")
        assert sc.parse_ids(sc.ids_from(p)) == ["B3", "B4"]


def test_ids_review3_without_reviser_brief():
    cases = {"b1h-r1__round3.md": ["N2", "N4"],              # "Open blocking findings to escalate to the user: N2 (open) and N4 (new)."
             "b1h-r4__round3.md": ["N3"],                    # "Open blocking findings: N3. Resolved: N2. Regressed: none."
             "b1h-r3-contaminated__round3.md": ["B2"]}       # "Blocking findings open: 1 (B2, new in round 3). Prior blocking findings: M2, ..."
    for name, want in cases.items():
        f = fx(name)
        assert sc.parse_ids(sc.ids_from(f)) == want, (name, sc.ids_from(f))
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "r.md"
        p.write_text("review: 3 of 3\n\n### N3 (blocking)\ntext\n\n- Open blocking findings: N3.\n\nverdict: FAIL\n")
        assert sc.parse_ids(sc.ids_from(p)) == ["N3"]
        p.write_text("review: 3 of 3\n\n### N5 (blocking)\ntext\n\nOpen blocking findings: none.\n\nverdict: FAIL\n")
        assert sc.parse_ids(sc.ids_from(p)) == []


def test_ids_fixtures_resolve_to_sections():
    fs = fail_fixtures()
    assert len(fs) >= 15
    for f in fs:
        t = f.read_text(errors="ignore")
        ids = sc.parse_ids(sc.ids_from(f))
        assert ids, f.name
        for fid in ids:
            assert sc.find_section(t, fid)[0] is not None, (f.name, fid)


# ------------------------------------------------------------------ 4(a): finding lists carry findings only
def build_list(path, clean=True):
    t = path.read_text(errors="ignore")
    ids = sc.parse_ids(sc.ids_from(path))
    parts = []
    for fid in ids:
        heading, body = sc.finding_block(t, fid, clean=clean)
        parts.append(f"### {fid}\n" + "\n".join([heading] + (body or "").splitlines()))
    return "\n\n".join(parts), ids


def test_no_banner_or_recommendation_survives_in_real_reports():
    contaminated_before = 0
    for f in fail_fixtures():
        text = f.read_text(errors="ignore")
        ids = sc.parse_ids(sc.ids_from(f))
        raw = "\n".join("\n".join(filter(None, sc.find_section(text, i))) for i in ids)         # the ab1 slicing
        if h.check_findings_text(raw):
            contaminated_before += 1
        out, _ = build_list(f)
        bad = h.check_findings_text(out)
        assert not bad, (f.name, bad[:3])
        for ln in out.splitlines():                                                              # explicit, independent of check_findings_text
            assert not re.match(r"^\s*={3,}", ln), (f.name, ln)
            assert not re.search(r"(?i)ARCHITECTURE ANALYSIS|ADVERSARIAL ANALYSIS|GUARD CONDITION BOUNDARY|FOLLOW-UP CANDIDATES|REVISER BRIEF", ln), (f.name, ln)
            assert not re.match(r"(?i)^\s*(?:[-*]\s*)?(?:\*\*)?\s*(recommendation|options?\b|reviser brief)", ln), (f.name, ln)
            assert not re.match(r"^\s*(?:[-*]\s*)?\([ab]\)\s", ln), (f.name, ln)
        parts = out.split("### ")
        assert len([p for p in parts if p.strip()]) >= len(ids)        # every finding is still there
        for fid in ids:
            assert re.search(rf"(?m)^### {re.escape(fid)}\n", out), (f.name, fid)
    assert contaminated_before >= 5, "the fixtures no longer exercise the ab1 contamination"


def test_clean_body_drops_advice_with_children():
    lines = ["- Location: SPEC:62", "- Grading sentence: An implementer ... wrong because Y.",
             "- Recommendation (either option):", "  - (a) keep the directory form", "  - (b) keep the file form", "  wrapped continuation",
             "- Option (b) is preferred because ...", "- Priority: High. Quality impact: x", "- Origin: introduced by the revision",
             "- Verification status: checked", "Reviser brief note: narrow P1", "- Stated texts:", "  - SPEC:62: \"x\""]
    out = sc.clean_body(lines)
    assert out == ["- Location: SPEC:62", "- Grading sentence: An implementer ... wrong because Y.", "- Stated texts:", "  - SPEC:62: \"x\""], out


def test_cut_block_stops_at_banners():
    lines = ["a", "b", "", "=== ARCHITECTURE ANALYSIS ===", "c"]
    assert sc.cut_block(lines) == ["a", "b"]
    assert sc.cut_block(["a", "## Reviser brief", "x"]) == ["a"]
    assert sc.cut_block(["a", "### === SOMETHING ===", "x"]) == ["a"]
    assert sc.cut_block(["a", "verdict: FAIL"]) == ["a"]


def make_run(name="d4-r1"):
    h.build("sonnet")
    return name


def test_findings_text_end_to_end():
    with env():
        run = make_run()
        for n, name in ((2, "b1-r6-contaminated__round2.md"), (3, "b1h-r4__round3.md")):
            (h.ws(run) / h.REVIEW / f"round{n}.md").write_text(fx(name).read_text())
        for n in (2, 3):
            out, ids = h.findings_text(run, n)
            assert ids and not h.check_findings_text(out), (n, h.check_findings_text(out)[:3])
            assert (h.ws(run) / h.REVIEW / f"findings-{n}.md").read_text().strip() == out.strip()
        # a contaminated list is refused, not launched
        try:
            h.check_findings_text("### N1\n=== ARCHITECTURE ANALYSIS ===") and (_ for _ in ()).throw(ValueError("bad"))
            raise AssertionError("not reached")
        except ValueError:
            pass


def test_merge_two_reports_clean():
    pairs = [("b1-r4__round1-a.md", "b1-r4__round1-b.md"), ("b1-r6__round1-b.md", "b1-r6__round1-c.md"),
             ("b1h-r3__round1-a.md", "b1h-r3__round1-c.md"), ("b1h-r4__round1-a.md", "b1h-r4__round1-c.md")]
    for a, b in pairs:
        with env():
            run = make_run()
            R = h.ws(run) / h.REVIEW
            (R / "round1-a.md").write_text(fx(a).read_text())
            (R / "round1-b.md").write_text(fx(b).read_text())
            mids = h.merge(run)
            assert mids, (a, b)
            text = (R / "findings-1.md").read_text()
            assert not h.check_findings_text(text), (a, b, h.check_findings_text(text)[:3])
            st = h.load(run)
            assert set(st["merge"]["reviewers"]) == {"a", "b"}
            assert st["merge"]["raw_count"] >= st["merge"]["merged_count"] >= 1
            assert all(re.match(r"M\d+$", m) for m in mids)
            assert "#### M1.a (round1-a.md" in text or "#### M1.a (round1-b.md" in text


def test_merge_dedups_same_defect_across_the_two_reviews():
    with env():
        run = make_run()
        R = h.ws(run) / h.REVIEW
        rep = ("review: 1 of 3\n\n### F1 (blocking): AC-1.1 requires a section on /sc:load\n- Texts: SPEC:195 and SPEC:112 contradict.\n"
               "- Grading sentence: An implementer ... wrong.\n\n## Reviser brief\n\nBlocking finding ids: F1.\n\nverdict: FAIL\n")
        (R / "round1-a.md").write_text(rep)
        (R / "round1-b.md").write_text(rep.replace("F1", "B7"))
        mids = h.merge(run)
        assert mids == ["M1"], mids
        assert h.load(run)["merge"]["raw_count"] == 2
        t = (R / "findings-1.md").read_text()
        assert "#### M1.a (round1-a.md F1)" in t and "#### M1.b (round1-b.md B7)" in t


# ------------------------------------------------------------------ 4(b): the verifier's confirmed line is authoritative
def test_confirmed_line_authoritative_over_multiple_rows():
    text = fx("b1h-r3__verify-1.md").read_text()
    ids = [f"M{i}" for i in range(1, 11)]
    table, ok = h.parse_verify(text, ids)
    assert table["M4"][0] == "reject"                      # the first row of M4 (M4.a) says reject ...
    fixed = h.reconcile_confirmed(table, ids, text)
    assert fixed["M4"][0] == "confirm"                     # ... the confirmed line (M4.b holds) wins
    assert [i for i in ids if fixed[i][0] == "confirm"] == ["M3", "M4", "M6", "M7", "M8", "M10"]
    assert fixed["M9"][0] == "reject"
    # the line also demotes a row that says confirm but is not named, and `none` confirms nothing
    syn = verify_reply(["M1", "M2"], ["M1", "M2"]).replace("confirmed: M1, M2", "confirmed: M1")
    t2, _ = h.parse_verify(syn, ["M1", "M2"])
    assert h.reconcile_confirmed(t2, ["M1", "M2"], syn)["M2"][0] == "reject"
    t3 = h.reconcile_confirmed(t2, ["M1", "M2"], syn.replace("confirmed: M1", "confirmed: none"))
    assert {v[0] for v in t3.values()} == {"reject"}


def test_ingest_vf_uses_confirmed_line():
    with env():
        run = make_run()
        st = h.load(run)
        st["log"]["VF1"] = {"finding_ids": ["M1", "M4"]}
        st["merge"] = {"groups": [{"mid": "M1", "theme": "other", "cited": [], "heading": "h", "members": []},
                                  {"mid": "M4", "theme": "other", "cited": [], "heading": "h", "members": []}],
                       "reviewers": {x: {"verdict": "FAIL", "sha256": "0"} for x in "ab"}}
        h.save(run, st)
        outp = h.out_path(run, "VF1")
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text("| id | f | e | o | verdict | reason |\n|---|---|---|---|---|---|\n"
                        "| M1 | x | yes | yes | confirm | ok |\n| M4 | M4.a: x | yes | no | reject | gap |\n| M4 | M4.b: y | yes | yes | confirm | holds |\n"
                        "confirmed: M1, M4\n")
        meta = h.ingest_vf(run, h.load(run), 1, outp)
        assert meta["confirmed"] == ["M1", "M4"] and not meta["rejected"], meta


# ------------------------------------------------------------------ lint pre-pass (item 1) and briefs (item 2)
def test_lint_code_is_the_pn2_lint():
    pn2 = AB.parents[1] / "p13/clones/pn2/src/superclaude/cli/review/lint.py"
    if pn2.exists():
        assert pn2.read_bytes() == (AB / "reqlint.py").read_bytes()
    spec_text = "# S\n\n| ID | R |\n|---|---|\n| FR-1 | a |\n\nAC-1.1 verifies FR-1 and FR-7.\n"
    md = L.render_md(L.run_lint(spec_text.encode(), L.parse_checks("REF")))
    assert "FR-7 is referenced but never defined" in md and md == L.render_md(L.run_lint(spec_text.encode(), L.parse_checks("REF")))


def test_lint_prepass_and_briefs():
    with env():
        h.build("sonnet")
        run = "d4-r1"
        out = adv(["--dry-run"])
        assert len(launches(out)) == 6                                   # 3 runs x (R1a, R1b) fit in MAX_CONCURRENT
        lint1 = h.ws(run) / h.lint_rel(1)
        assert lint1.exists() and lint1.read_text().startswith("lint: superclaude review lint, review-lint/1")
        for x in "ab":                                                    # the reviewers read it from their own sandbox
            assert (h.run_dir(run) / f"r1{x}" / "ws" / h.lint_rel(1)).read_text() == lint1.read_text()
        a = (h.run_dir(run) / "PROMPT-R1a.md").read_text()
        b = (h.run_dir(run) / "PROMPT-R1b.md").read_text()
        assert f"Values: candidate={h.SPEC}, lint={h.lint_rel(1)}." in a
        assert h.SWEEP not in a and h.SWEEP in b
        assert b.replace(" " + h.SWEEP, "").replace("/r1b", "/r1a") == a            # R1b = R1a + exactly one sentence
        assert ("In addition, check every acceptance criterion and every live-check step one by one: for each, state whether it can pass as written "
                "for every command and phase it covers, and record any that cannot as a finding under the same blocking rule.") == h.SWEEP
        # ab1 brief + lint value only
        assert h.brief_first("OUT").replace(f", lint={h.lint_rel(1)}.", ".") == (
            f"Run /sc:spec-panel @{h.SPEC} {h.FLAGS} . Review per the FIRST-REVIEW prompt in {h.RULES_PTR}. Values: candidate={h.SPEC}.\n"
            f"Write the full report to OUT. Do not edit anything else. {h.CTX}")
        rec = h.load(run)["log"]["LINT1"]
        assert rec["findings"] == 0 and rec["checks"] == ["REF"] and rec["stratum"] == "sonnet"
        # lint-2 / lint-3 after a revision, referenced by the re-review brief
        spec = h.ws(run) / h.SPEC
        spec.write_text(spec.read_text() + "\n\nAC-9.9 verifies FR-77.\n")
        h.prep(run, "R2")
        assert (h.ws(run) / h.lint_rel(2)).exists() and h.load(run)["log"]["LINT2"]["findings"] >= 1
        assert f"lint={h.lint_rel(2)}" in (h.run_dir(run) / "PROMPT-R2.md").read_text()
        h.prep(run, "R3")
        assert f"lint={h.lint_rel(3)}" in (h.run_dir(run) / "PROMPT-R3.md").read_text() and (h.ws(run) / h.lint_rel(3)).exists()
        assert h.load(run)["log"]["LINT3"]["spec_sha256"] == h.sha(spec)


def test_rules_file_has_lint_bullets_and_k2_wording():
    r = (AB / "frozen" / "rules.md").read_text()
    assert r.count("- **Lint evidence**") == 2 and "Two first reviews" in r
    assert not re.search(r"(?i)\bthree\b", r)


# ------------------------------------------------------------------ item 5: tokens by prompt text
def write_transcript(path, first_user, msgs, model="claude-sonnet-5-5", done=True):
    rows = [{"type": "user", "message": {"role": "user", "content": first_user}}]
    for mid, tokens in msgs:           # one line per content block: a message id repeats
        for ot in tokens:
            rows.append({"type": "assistant", "message": {"role": "assistant", "id": mid, "model": model, "usage": {"output_tokens": ot},
                                                          "content": [{"type": "text", "text": "x"}]}})
    if done:
        rows.append({"type": "assistant", "message": {"role": "assistant", "id": "last", "model": model, "usage": {"output_tokens": 5},
                                                      "content": [{"type": "text", "text": "DONE /x/round1.md"}]}})
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def test_tokens_by_prompt_text_and_short_launch():
    with env() as tmp:
        h.build("sonnet")
        adv(["--dry-run"])
        tdir = tmp / "tasks"
        tdir.mkdir()
        h.TASKS_GLOB = str(tdir / "*.output")
        pa = (h.run_dir("d4-r1") / "PROMPT-R1a.md").read_text()
        pb = h.run_dir("d4-r1") / "PROMPT-R1b.md"
        pc = (h.run_dir("d4-r2") / "PROMPT-R1a.md").read_text()
        # pasted prompt; message id m1 appears on three lines (three content blocks) with growing output_tokens: counts once, at its max
        write_transcript(tdir / "a.output", pa, [("m1", [10, 40, 90]), ("m2", [7, 7])])
        # same prompt with a wrapper prefix
        write_transcript(tdir / "c.output", "<ctx>\n" + pc + "\n</ctx>", [("n1", [100])])
        # short launch message resolving the path
        write_transcript(tdir / "b.output", f"Read {pb} and follow it exactly", [("k1", [25, 30])])
        # unrelated transcript and a wrong-model transcript for the same prompt
        write_transcript(tdir / "z.output", "something else entirely", [("z1", [999])])
        write_transcript(tdir / "w.output", pa, [("w1", [5000])], model="claude-haiku-5-5")
        idx = h.scan_by_prompt()
        assert set(idx) == {("d4-r1", "R1a"), ("d4-r1", "R1b"), ("d4-r2", "R1a")}, set(idx)
        best = h.pick(idx[("d4-r1", "R1a")], "sonnet")
        assert best["tokens"] == 90 + 7 + 5 and best["done"]                     # max per id once: m1 90, m2 7, last 5
        assert h.pick(idx[("d4-r1", "R1b")], "sonnet")["tokens"] == 30 + 5
        assert h.pick(idx[("d4-r2", "R1a")], "sonnet")["tokens"] == 100 + 5
        st = h.load("d4-r1")
        st["log"]["R1a"] = {"output_exists": True}
        st["log"]["R1b"] = {"output_exists": True}
        h.save("d4-r1", st)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            h.tokens_cmd("d4-r1")
        st = h.load("d4-r1")
        assert st["log"]["R1a"]["output_tokens"] == 102 and st["log"]["R1b"]["output_tokens"] == 35
        assert "loop 137" in buf.getvalue()
        # resolve_short: a runs/<run>/<sandbox>/PROMPT.md style path takes the step from the sandbox directory
        table = h.prompt_table()
        assert h.resolve_short(f"Read {h.run_dir('d4-r3')}/vf2/PROMPT.md and follow it exactly", table) == ("d4-r3", "VF2")
        assert h.resolve_short("hello", table) is None


# ------------------------------------------------------------------ item 6/D3: names, strata, AUD model
def test_run_names_strata_and_aud_model():
    with env():
        h.build("sonnet")
        h.build("haiku")
        names = [p.name for p in h.RUNS.iterdir()]
        assert sorted(n for n in names if n.startswith("d4-")) == [f"d4-r{i}" for i in range(1, 7)]
        assert sorted(n for n in names if n.startswith("d4h-")) == [f"d4h-r{i}" for i in range(1, 5)]
        for run in h.all_runs():
            st = h.load(run)
            assert st["stratum"] == ("haiku" if "h-" in run else "sonnet")
            assert h.expected_model(st, "AUD") == "sonnet" and h.expected_model(st, "AUD2") == "sonnet"
            assert h.expected_model(st, "R2") == st["stratum"]
        assert h.run_names("sonnet", True) == ["d4-r7", "d4-r8", "d4-r9"]
        out = adv(["--dry-run"])
        assert all(" model=sonnet" in ln for ln in launches(out))                 # the first 6 launches are Sonnet runs


def test_extension_rule_d4():
    with env() as tmp:
        try:
            h.build("sonnet", True)
            raise AssertionError("extension must be refused without an INCONCLUSIVE n=6 metrics.json")
        except SystemExit:
            pass
        (tmp / "metrics.json").write_text(json.dumps({"sonnet": {"n_runs": 6, "extension_eligible": True}}))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            h.build("sonnet", True)
        assert sorted(p.name for p in h.RUNS.iterdir()) == ["d4-r7", "d4-r8", "d4-r9"]
        try:
            h.build("sonnet", True)
            raise AssertionError("a second extension must be refused")
        except SystemExit:
            pass


# ------------------------------------------------------------------ D2 / D6 constants and the analysis convention
def test_decision_constants_d2_d6():
    d = json.load(open(AB / "decision.json"))
    assert (d["A_BASE"], d["AUD_BASE"], d["B_BASE"]) == (100424, 69044, 169468)
    assert d["N_SONNET"] == 6 and d["N_HAIKU"] == 4 and d["N_EXTEND"] == 3
    assert round((2.0 * 169468 - 69044) / 100424, 2) == d["rules"]["DROP2_RLOOP_LIMIT"] == 2.69
    assert d["MIN_COMPLETED"] == {"6": 5, "9": 8}
    assert d["haiku"]["harness_fail_margin"] == 0.25
    src = (AB / "advance.py").read_text() + (AB / "harness.py").read_text()
    assert not re.search(r"(?i)abort|TaskStop|kill", src), "no cost kill anywhere"
    assert "R_LOOP" not in (AB / "advance.py").read_text()                      # cost is read only in analyze/decide


def rec_(run, loop, aud_tok, blk, verdict="FAIL"):
    return {"run": run, "stratum": "sonnet", "lost": False, "complete": True, "loop_end": "VERIFIED-PASS", "final_bytes": 58500,
            "loop_tokens": loop, "aud_tokens": [aud_tok, aud_tok], "vf": {}, "audits": [
                {"step": "AUD", "verdict": verdict, "findings": [{"id": f"B{i}", "theme": "other"} for i in range(blk)]},
                {"step": "AUD2", "verdict": verdict, "findings": [{"id": f"B{i}", "theme": "other"} for i in range(blk)]}]}


def test_loop_only_cost_decides_and_b_is_reported():
    dec = json.load(open(AB / "decision.json"))
    base = {"B_BLK": 1.5, "B_AUDFAIL": h.Fraction(5, 6), "B_THEME": h.Fraction(5, 6), "B_GROWTH": 0.0141, "n_audits": 6}
    recs = [rec_(f"d4-r{i}", 100424, 69044, 0, "PASS") for i in range(1, 7)]
    o = h.decide(recs, dec, base, 6)
    assert abs(o["R_LOOP"] - 1.0) < 1e-9 and abs(o["R_B"] - 1.0) < 1e-9
    big_aud = [rec_(f"d4-r{i}", 100424, 900000, 0, "PASS") for i in range(1, 7)]
    o2 = h.decide(big_aud, dec, base, 6)
    assert o2["R_LOOP"] == o["R_LOOP"] and o2["R_B"] > 5 and o2["outcome"] == o["outcome"]       # B is reported, never decides
    costly = [rec_(f"d4-r{i}", 300000, 69044, 1) for i in range(1, 7)]
    o3 = h.decide(costly, dec, base, 6)
    assert o3["R_LOOP"] > 2.69 and o3["outcome"] == "DROP" and "DROP-2" in o3["rule"]         # cost clause, post hoc
    few = h.decide(recs[:4], dec, base, 6)
    assert few["outcome"] == "INCONCLUSIVE"


# ------------------------------------------------------------------ whole loop on fixtures, then analyze
def test_full_loop_on_fixtures_and_analyze():
    with env() as tmp:
        h.build("sonnet")
        run = "d4-r1"
        adv()
        fake(run, "R1a", fx("b1-r4__round1-a.md").read_text())
        fake(run, "R1b", fx("b1-r4__round1-b.md").read_text())
        out = adv()
        assert not any(ln.startswith(("MANUAL", "LOST")) for ln in out.splitlines()), out
        st = h.load(run)
        assert st["merge"]["done"] and "VF1" in st["prepared"]
        assert not h.check_findings_text((h.ws(run) / h.REVIEW / "findings-1.md").read_text())
        vf1 = (h.run_dir(run) / "PROMPT-VF1.md").read_text()
        assert not h.check_findings_text(vf1[vf1.index("Findings:"):vf1.index("Write your full reply")])
        ids1 = st["log"]["VF1"]["finding_ids"]
        fake(run, "VF1", verify_reply(ids1, ids1[:-1]))
        out = adv()
        st = h.load(run)
        assert st["log"]["VF1"]["confirmed"] == ids1[:-1] and "V1" in st["prepared"]
        round1 = (h.ws(run) / h.REVIEW / "round1.md").read_text()
        assert not re.search(r"(?m)^={3,}", round1), "merged round1.md still carries banner sections"
        assert "over two independent first reviews" in round1 and "round1-b.md verdict" in round1 and "round1-c.md" not in round1
        fake(run, "V1", "revise1\n")
        adv()
        st = h.load(run)
        assert "R2" in st["prepared"] and (h.ws(run) / h.lint_rel(2)).exists()
        fake(run, "R2", fx("b1-r6-contaminated__round2.md").read_text())
        adv()
        st = h.load(run)
        assert "VF2" in st["prepared"], st["prepared"]
        ids2 = st["log"]["VF2"]["finding_ids"]
        assert ids2 == ["N1", "N2"], ids2
        vf2 = (h.run_dir(run) / "PROMPT-VF2.md").read_text()
        assert not h.check_findings_text(vf2[vf2.index("Findings:"):vf2.index("Write your full reply")])
        fake(run, "VF2", verify_reply(ids2, ids2))
        adv()
        fake(run, "V2", "revise2\n")
        adv()
        assert "R3" in h.load(run)["prepared"] and (h.ws(run) / h.lint_rel(3)).exists()
        fake(run, "R3", fx("b1h-r4__round3.md").read_text())            # review 3, no Reviser brief: "Open blocking findings: N3" (ab1 needed setids)
        out = adv()
        assert not any(ln.startswith("MANUAL") for ln in out.splitlines()), out
        st = h.load(run)
        assert st["log"]["VF3"]["finding_ids"] == ["N3"] and not st["manual"]
        vf3 = (h.run_dir(run) / "PROMPT-VF3.md").read_text()
        assert not h.check_findings_text(vf3[vf3.index("Findings:"):vf3.index("Write your full reply")])
        fake(run, "VF3", verify_reply(["N3"], []))
        adv()
        st = h.load(run)
        assert st["loop_end"] == "VERIFIED-PASS" and {"AUD", "AUD2"} <= set(st["prepared"])
        for step in ("AUD", "AUD2"):
            fake(run, step, fx("b1-r4__round1-a.md").read_text())
        for _ in range(3):                                   # AUD2 is launched once AUD frees a slot
            out = adv()
            st = h.load(run)
            if st["complete"]:
                break
        assert st["complete"], out
        for s in ("R1a", "R1b", "VF1", "V1", "R2", "VF2", "V2", "R3", "VF3", "AUD", "AUD2"):
            assert st["log"][s]["stratum"] == "sonnet"
        assert [st["log"].get(f"LINT{i}", {}).get("findings") is not None for i in (1, 2, 3)] == [True, True, True]
        m = h.analyze()
        assert (tmp / "RESULTS-tables.md").exists() and (tmp / "metrics.json").exists()
        tables = (tmp / "RESULTS-tables.md").read_text()
        assert "Per-theme capture, k=2" in tables and "lint findings 1/2/3" in tables
        assert m["sonnet"]["outcome"] == "INCONCLUSIVE"                  # one run only: fewer than 5 completed


def main():
    fns = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    failed = 0
    for n, f in fns:
        try:
            f()
            print("PASS", n)
        except Exception:
            failed += 1
            print("FAIL", n)
            traceback.print_exc()
    print(f"{len(fns) - failed}/{len(fns)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
