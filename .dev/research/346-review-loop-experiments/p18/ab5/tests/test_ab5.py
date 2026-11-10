"""Offline tests of the ab5 tooling (two arms: variant panel = d5-r*, variant full = d5f-r*). No pytest needed (plain asserts):
  cd $SP/p18/ab5 && python3 tests/test_ab5.py          (pytest also collects the test_* functions if it is installed)
Fixtures (tests/fixtures): real reports from p12/ab1 (copied by ab4), from the ab4 runs (ab4-d4-*) and from the PN1 runs (pn1-b1-*)."""
import contextlib
import hashlib
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
SP = AB.parents[1]
sys.path.insert(0, str(AB))
import advance  # noqa: E402
import full  # noqa: E402
import harness as h  # noqa: E402
import reqlint as L  # noqa: E402
import score_themes as sc  # noqa: E402

RV = ".dev/orca-command-refactor/review/"
RIDS = ["t1b-1", "t2-1", "t3-1", "t4-1"]
PN1_RIDS = ["t1b-1", "t2-1", "t3-1", "t3-2"]          # PN1 fixture reports, mapped onto the ab5 slots by position
DEC = json.load(open(AB / "decision.json"))
TIERS = json.load(open(AB / "frozen/review-tiers.default.json"))
SONNET = DEC["live_alias_map"]["claude-gw-tier1b[1m]"]["model"]                       # model names come from the data, not the tests
HAIKU = TIERS["environments"][DEC["panel"]["environment"]]["stand_ins"]["tier2"][0]


def strip_live(res):
    out = json.loads(json.dumps(res))
    for r in out["reviewers"]:
        r.pop("live_model", None)
        r.pop("live_name", None)
    return out


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
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def adv(argv=()):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        advance.main(list(argv))
    return buf.getvalue()


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


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


def verify_reply(ids, confirmed):
    lines = ["| id | found | exists | follows | verdict | reason |", "|---|---|---|---|---|---|"]
    for fid in ids:
        lines.append(f"| {fid} | text | yes | yes | {'confirm' if fid in confirmed else 'reject'} | because |")
    lines.append("confirmed: " + (", ".join(confirmed) if confirmed else "none"))
    return "\n".join(lines) + "\n"


def adj_reply(mapping, verdict="confirmed"):
    return "notes\n\n```adj-v1\n" + "\n".join(json.dumps({"x": x, "verdict": verdict, "reason": "r"}) for x in mapping) + "\n```\n"


# ------------------------------------------------------------------ copies, hashes, rules
def test_copied_sources_are_byte_identical():
    assert (AB / "score_themes.py").read_bytes() == (SP / "p16/ab4/score_themes.py").read_bytes()      # ids_from, finding_block, clean_body
    assert (AB / "reqlint.py").read_bytes() == (SP / "p16/ab4/reqlint.py").read_bytes()
    pn1 = SP / "p13/clones/pn1/src/superclaude/cli/review"
    if pn1.exists():
        assert (AB / "pn1_panel.py").read_bytes() == (pn1 / "panel.py").read_bytes()
        for f in ("findings.py", "ledger.py", "merge_cmd.py", "ledger_cmd.py"):
            assert (AB / "vendor/superclaude/cli/review" / f).read_bytes() == (pn1 / f).read_bytes(), f
        for f in ("review-panel.default.json", "review-tiers.default.json"):
            assert (AB / "frozen" / f).read_bytes() == (pn1 / "data" / f).read_bytes(), f
    d = json.load(open(AB / "decision.json"))
    fz = d["frozen"]
    for name, key in (("command.md", "cmd_sha"), ("audit-rules.md", "aud_rules_sha"), ("rules.md", "rules_sha"), ("rules-full.md", "rules_full_sha"),
                      ("rules-pn1.md", "rules_pn1_sha"), ("review-panel.default.json", "pn1_panel_template_sha"), ("review-panel.ab5.json", "panel_template_sha"), ("review-tiers.default.json", "panel_tiers_sha")):
        assert sha(AB / "frozen" / name) == fz[key], name
    assert fz["cmd_sha"] == fz["aud_cmd_sha"] == "e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494"          # frozen audit command
    assert fz["aud_rules_sha"] == "3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8"                         # frozen audit rules
    for f in ("command.md", "audit-rules.md", "rules-ab1.md", "rules-pn2.md"):
        assert (AB / "frozen" / f).read_bytes() == (SP / "p16/ab4/frozen" / f).read_bytes(), f
    assert h.SPEC_SHA == "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
    pn1_rules = SP / "p13/ab1/runs/b1-r1/home/.claude/rules/prompts/document_review_loop_prompts.md"
    if pn1_rules.exists():
        assert (AB / "frozen/rules-pn1.md").read_bytes() == pn1_rules.read_bytes()


def test_rules_files_wording():
    r = (AB / "frozen/rules.md").read_text()
    assert r.count("- **Lint evidence**") == 2 and "Four first reviews" in r and "four reports" in r
    assert not re.search(r"(?i)\bthree\b", r)
    ab1 = (AB / "frozen/rules-ab1.md").read_text()
    import make_rules
    assert make_rules.t == r                                                     # rebuildable from the two sources
    diff = [ln for ln in r.splitlines() if ln not in ab1.splitlines()]
    assert len(diff) == 6, diff                                                  # 2 lint bullets + 4 changed lines (5 substitutions)
    f = (AB / "frozen/rules-full.md").read_text()
    assert make_rules.full_rules() == f and f.count("- **Lint evidence**") == 2
    assert f.replace("\n" + make_rules.lint[0], "").replace("\n" + make_rules.lint[1], "") == (AB / "frozen/rules-pn1.md").read_text()


def test_panel_resolution_equals_pn1():
    """pn1_panel + frozen template/tiers reproduce PN1's own panel.json / panel-rr.json byte for byte (as JSON) for real PN1 runs."""
    with env():
        for run in ("b1-r1", "b1-r4"):
            p = SP / "p13/ab1/runs" / run
            if not p.exists():
                continue
            pn1 = dict(template="review-panel.default.json", sha_key="pn1_panel_template_sha")
            assert strip_live(h.resolve_panel(run, "first", **pn1)) == json.load(open(p / "panel.json"))
            assert strip_live(h.resolve_panel(run, "re-review", **pn1)) == json.load(open(p / "panel-rr.json"))


def test_panel_template_one_reviewer_per_tier():
    tpl = json.load(open(AB / "frozen/review-panel.ab5.json"))
    assert [(s["slot_id"], s["tier"], s["count"]) for s in tpl["slots"]] == [("t1b", "tier1b", 1), ("t2", "tier2", 1), ("t3", "tier3", 1), ("t4", "tier4", 1)]
    with env():
        res = h.resolve_panel("d5-r1", "first")
        rv = res["reviewers"]
        assert [r["reviewer_id"] for r in rv] == RIDS and [r["tier"] for r in rv] == ["tier1b", "tier2", "tier3", "tier4"]
        assert [r["alias"] for r in rv] == [f"claude-gw-{x}[1m]" for x in ("tier1b", "tier2", "tier3", "tier4")]
        assert not any(r["tier"] == "tier1a" for r in rv)
        # same compute as PN1's panel: 1 primary model + 3 stand-ins of one model (only the slot labels change)
        pn1 = h.resolve_panel("d5-r1", "first", template="review-panel.default.json", sha_key="pn1_panel_template_sha")["reviewers"]
        assert sorted((r["model"], r["stand_in"]) for r in rv) == sorted((r["model"], r["stand_in"]) for r in pn1)
        assert [r["stand_in"] for r in rv] == [False, True, True, True] and len({r["model"] for r in rv[1:]}) == 1


# ------------------------------------------------------------------ OWNER RULE: no Fable / Tier 0, nothing above Sonnet in ab5
def test_no_forbidden_or_above_opus_model_anywhere():
    tier0 = re.compile(r"(?i)fable|tier0\b|tier-0|tier 0")
    with env() as tmp:
        quiet(h.build, "sonnet", False, "panel")
        quiet(h.build, "sonnet", False, "full")
        adv(["--dry-run"])
        for run in h.all_runs():
            st = h.load(run)
            for step in h.STEPS:
                m = h.expected_model(st, step)
                assert not tier0.search(m) and "opus" not in m.lower(), (run, step, m)
                assert m in ("sonnet", "haiku"), (run, step, m)
            for pr in (st["panel"], st["panel_rr"]):
                for r in pr["reviewers"]:
                    for k in ("model", "launch", "alias", "tier", "model_name"):
                        assert not tier0.search(str(r[k])) and "opus" not in str(r[k]).lower(), (run, r)
            assert all(v in ("sonnet", "haiku") for v in st["models"].values()), st["models"]
            for p in (h.run_dir(run) / "panel.json", h.run_dir(run) / "panel-rr.json"):
                assert not tier0.search(p.read_text()) and "opus" not in p.read_text().lower()
        # Haiku stratum code path (not built) also stays clear
        st = dict(h.load("d5-r1"), stratum="haiku", loop_model="haiku")
        assert {h.expected_model(st, s) for s in h.STEPS} <= {"sonnet", "haiku"}
        assert h.expected_model(st, "ADJ") == "haiku" and h.expected_model(h.load("d5-r1"), "ADJ") == "sonnet"
        # the guard refuses a forbidden model
        bad = h.load("d5-r1")
        bad["loop_model"] = "fable"
        for m in ("fable", "opus", "claude-opus-5-5"):
            bad["loop_model"] = m
            try:
                h.expected_model(bad, "V1")
                raise AssertionError("forbidden model accepted: " + m)
            except ValueError:
                pass
        d = json.load(open(tmp / "decision.json"))
        assert all(not tier0.search(v) for v in d["panel"]["adj_model"].values())
        assert all(not tier0.search(str(s)) for k, v in d["lanes"].items() if isinstance(v, list) for s in v)
    for f in ("harness.py", "advance.py", "full.py", "decision.json"):
        txt = (AB / f).read_text()
        for ln in txt.splitlines():                                   # 'fable' may appear only in the forbidden list and its comments
            if re.search(r"(?i)\bfable\b", ln):
                assert re.search(r"(?i)forbid|OWNER RULE|PN1 used|changed condition|no Fable|\"fable\",$|\"patterns\"", ln), (f, ln)
    led = AB / "launch-ledger.jsonl"
    if led.exists():
        for ln in led.read_text().splitlines():
            m = json.loads(ln)["model"]
            assert not tier0.search(m) and "opus" not in m


def test_mock_live_switch_changes_only_models_and_labels():
    """OWNER 2026-11-10: switching mock -> live = live_alias_map + reviewer_models.stand_in only; it changes only the resolved model
    fields (model, model_name, launch, stand_in) and the lane labels; no alias resolves to a Tier 0 model or above Opus."""
    tier0 = re.compile(r"(?i)fable|tier0\b")
    ceiling = DEC["live_alias_map"]["claude-gw-tier1a[1m]"]["model"]                          # the allowed ceiling (Opus)
    with env() as tmp:
        mock = h.resolve_panel("d5-r1", "first")
        assert [r["stand_in"] for r in mock["reviewers"]] == [False, True, True, True]
        d = json.load(open(tmp / "decision.json"))
        d["reviewer_models"]["stand_in"] = False
        live = h.apply_model_map(strip_live(mock), d)
        changed = {"model", "model_name", "launch", "stand_in"}
        for a, b in zip(mock["reviewers"], live["reviewers"]):
            diff = {k for k in a if a[k] != b[k]}
            assert diff <= changed, diff
            assert b["model"] == d["live_alias_map"][b["alias"]]["model"] and b["stand_in"] is False
        assert {k: v for k, v in mock.items() if k != "reviewers"} == {k: v for k, v in live.items() if k != "reviewers"}
        assert {r["reviewer_id"]: h.lane_of("R1." + r["reviewer_id"], d) for r in live["reviewers"]} == \
               {r["reviewer_id"]: h.lane_of("R1." + r["reviewer_id"], DEC) for r in mock["reviewers"]}         # lanes are by slot: unchanged
        rec_m = [{"panel_reviewers": mock["reviewers"]}]
        rec_l = [{"panel_reviewers": live["reviewers"]}]
        for r in mock["reviewers"][1:]:
            lm, ll = h.slot_label(r["reviewer_id"], DEC, rec_m), h.slot_label(r["reviewer_id"], d, rec_l)
            name = d["live_alias_map"][r["alias"]]["name"]
            assert name in lm and name in ll and "(stand-in)" in lm and "(stand-in)" not in ll and lm != ll
        # a changed map changes only the model fields
        d2 = json.loads(json.dumps(d))
        d2["live_alias_map"]["claude-gw-tier2[1m]"] = {"model": "other-model-x", "name": "Other X", "launch": "gw2"}
        live2 = h.apply_model_map(strip_live(mock), d2)
        assert live2["reviewers"][1]["model"] == "other-model-x" and live2["reviewers"][0] == live["reviewers"][0]
        # no alias resolves to Tier 0 or above the ceiling
        order = [DEC["live_alias_map"][a]["model"] for a in ("claude-gw-tier1a[1m]",)]
        for alias, m in d["live_alias_map"].items():
            if alias.startswith("_"):
                continue
            assert not tier0.search(m["model"] + m["name"] + alias), alias
        assert ceiling in order and all(r["model"] != ceiling for r in live["reviewers"])           # no panel slot uses the ceiling
        tpl = json.load(open(AB / "frozen/review-panel.default.json"))
        for slot in tpl["slots"]:                                                                  # every slot's alias has a live mapping
            assert TIERS["aliases"][slot["tier"]]["alias"] in DEC["live_alias_map"], slot


# ------------------------------------------------------------------ panel briefs, names, strata
def test_panel_briefs_tiers_lint_and_sweep():
    with env():
        quiet(h.build, "sonnet")
        run = "d5-r1"
        out = adv(["--dry-run"])
        assert len(launches(out)) == 24                                          # 6 runs x 4 panel reviewers
        st = h.load(run)
        assert [r["reviewer_id"] for r in st["panel"]["reviewers"]] == RIDS
        amap = DEC["live_alias_map"]
        assert {r["reviewer_id"]: (r["tier"], r["alias"], r["model"], r["stand_in"], r["live_model"]) for r in st["panel"]["reviewers"]} == {
            "t1b-1": ("tier1b", "claude-gw-tier1b[1m]", SONNET, False, amap["claude-gw-tier1b[1m]"]["model"]),
            "t2-1": ("tier2", "claude-gw-tier2[1m]", HAIKU, True, amap["claude-gw-tier2[1m]"]["model"]),
            "t3-1": ("tier3", "claude-gw-tier3[1m]", HAIKU, True, amap["claude-gw-tier3[1m]"]["model"]),
            "t4-1": ("tier4", "claude-gw-tier4[1m]", HAIKU, True, amap["claude-gw-tier4[1m]"]["model"])}
        assert not any(r["slot_id"] == "t1a" for r in st["panel"]["reviewers"])                    # no t1a slot added
        mine = [ln for ln in launches(out) if "/d5-r1/" in ln]
        assert [ln.split("PROMPT-")[1] for ln in mine] == ["R1.t1b-1.md model=sonnet", "R1.t2-1.md model=haiku", "R1.t3-1.md model=haiku", "R1.t4-1.md model=haiku"]
        lint1 = h.ws(run) / h.lint_rel(1)
        assert lint1.exists()
        texts = {}
        for rid in RIDS:
            assert (h.run_dir(run) / f"r1-{rid}" / "ws" / h.lint_rel(1)).read_text() == lint1.read_text()
            texts[rid] = (h.run_dir(run) / f"PROMPT-R1.{rid}.md").read_text()
            assert f"Values: candidate={h.SPEC}, lint={h.lint_rel(1)}." in texts[rid]
            assert str(h.run_dir(run) / f"r1-{rid}") in texts[rid]
        assert h.SWEEP in texts["t1b-1"] and all(h.SWEEP not in texts[r] for r in RIDS[1:])
        for r in RIDS[1:]:                                                       # the other three = plain brief, only the sandbox differs
            assert texts["t1b-1"].replace(" " + h.SWEEP, "").replace("/r1-t1b-1", f"/r1-{r}") == texts[r]
        assert h.brief_first("OUT").replace(f", lint={h.lint_rel(1)}.", ".") == (
            f"Run /sc:spec-panel @{h.SPEC} {h.FLAGS} . Review per the FIRST-REVIEW prompt in {h.RULES_PTR}. Values: candidate={h.SPEC}.\n"
            f"Write the full report to OUT. Do not edit anything else. {h.CTX}")                       # = PN1 brief("R1") + lint value
        assert not st["launched"] and set(st["prepared"]) == {f"R1.{r}" for r in RIDS}


def test_names_strata_haiku_refused_and_extension():
    with env() as tmp:
        quiet(h.build, "sonnet")
        quiet(h.build, "sonnet", False, "full")
        assert [r for r in h.all_runs()] == [x for i in range(1, 7) for x in (f"d5-r{i}", f"d5f-r{i}")]      # arms interleave
        try:
            h.build("haiku")
            raise AssertionError("haiku stratum must be refused")
        except SystemExit as e:
            assert "Sonnet stratum only" in str(e)
        for run in h.all_runs():
            st = h.load(run)
            assert st["stratum"] == "sonnet" and st["variant"] == ("full" if run.startswith("d5f") else "panel")
            assert h.expected_model(st, "AUD") == h.expected_model(st, "AUD2") == "sonnet"
        assert h.run_names("haiku", False) == [f"d5h-r{i}" for i in range(1, 5)]
        assert h.run_names("sonnet", True, "full") == ["d5f-r7", "d5f-r8", "d5f-r9"]
        try:
            h.build("sonnet", True)
            raise AssertionError("extension must be refused without an INCONCLUSIVE n=6 metrics.json")
        except SystemExit:
            pass
        (tmp / "metrics.json").write_text(json.dumps({"panel": {"sonnet": {"n_runs": 6, "extension_eligible": True}}}))
        quiet(h.build, "sonnet", True)
        assert (h.RUNS / "d5-r9").exists() and not (h.RUNS / "d5f-r7").exists()


# ------------------------------------------------------------------ ids parsing on real fixtures (ab4 and PN1 runs)
def test_ids_on_ab4_and_pn1_fixtures():
    want_ab4 = {"ab4-d4-r1__round1-a.md": ["B1"], "ab4-d4-r1__round1-b.md": ["B1", "B2", "B3", "B4", "B5"], "ab4-d4-r3__round1-a.md": ["B-1"],
                "ab4-d4-r3__round1-b.md": ["F-1", "F-2", "F-3", "F-4", "F-5"], "ab4-d4-r6__round1-a.md": ["R1-B1", "R1-B2"],
                "ab4-d4-r6__round1-b.md": ["F1", "F2", "F3", "F4", "F5"], "ab4-d4h-r2__round2.md": ["M1", "M9", "M16", "N1", "N2"]}
    for name, want in want_ab4.items():
        assert sc.parse_ids(sc.ids_from(fx(name))) == want, (name, sc.ids_from(fx(name)))
    # ab4's state recorded the same parse when the run was live
    st = SP / "p16/ab4/runs/d4-r1/state.json"
    if st.exists():
        j = json.load(open(st))
        assert sc.parse_ids(j["log"]["R1b"]["blocking_ids"]) == want_ab4["ab4-d4-r1__round1-b.md"]
    # PN1 reports: ids_from agrees with the PN1 findings block on 8 of 12; the 4 known disagreements are PN1-format prose
    agree, differ = 0, {}
    for f in sorted(FX.glob("pn1-*round1-*.md")):
        t = f.read_text()
        blk = [x["id"] for x in full.F.parse_block(t)["findings"] if x["blocking"]]
        got = sc.parse_ids(sc.ids_from(f))
        if got == blk:
            agree += 1
        else:
            differ[f.name] = (got, blk)
    assert agree == 8, differ
    assert set(differ) == {"pn1-b1-r1__round1-t3-1.md", "pn1-b1-r3__round1-t2-1.md", "pn1-b1-r3__round1-t3-1.md", "pn1-b1-r4__round1-t1b-1.md"}, differ
    assert sc.parse_ids(sc.ids_from(fx("pn1-b1-r1__round2-t1b-1.md"))) == ["N1"]


# ------------------------------------------------------------------ merge over four reports (panel variant), dedup, ADJ prep
FOUR = ["b1-r4__round1-a.md", "b1-r4__round1-b.md", "b1-r6__round1-b.md", "b1-r6__round1-c.md"]


def put_panel(run, names):
    R = h.ws(run) / h.REVIEW
    for rid, name in zip(RIDS, names):
        (R / f"round1-{rid}.md").write_text(fx(name).read_text())


def test_merge_four_reports_clean_and_dedup():
    with env():
        quiet(h.build, "sonnet")
        run = "d5-r1"
        put_panel(run, FOUR)
        mids = quiet(h.merge, run)
        R = h.ws(run) / h.REVIEW
        text = (R / "findings-1.md").read_text()
        assert mids and not h.check_findings_text(text), h.check_findings_text(text)[:3]
        st = h.load(run)
        assert set(st["merge"]["reviewers"]) == set(RIDS)
        assert st["merge"]["raw_count"] >= st["merge"]["merged_count"] >= 1
        srcs = set(re.findall(r"\((round1-t[\w-]+\.md) ", text))
        assert srcs == {f"round1-{r}.md" for r in RIDS}, srcs
        assert st["merge"]["reviewers"]["t2-1"]["model"] == "haiku" and st["merge"]["reviewers"]["t1b-1"]["model"] == "sonnet"
    with env():                                                                  # the same defect in all four reports -> one M1 with 4 sub-entries
        quiet(h.build, "sonnet")
        run = "d5-r1"
        rep = ("review: 1 of 3\n\n### F1 (blocking): AC-1.1 requires a section on /sc:load\n- Texts: SPEC:195 and SPEC:112 contradict.\n"
               "- Grading sentence: An implementer ... wrong.\n- Recommendation: drop it\n\n=== ARCHITECTURE ANALYSIS ===\nnoise\n\n## Reviser brief\n\nBlocking finding ids: F1.\n\nverdict: FAIL\n")
        R = h.ws(run) / h.REVIEW
        for i, rid in enumerate(RIDS):
            (R / f"round1-{rid}.md").write_text(rep.replace("F1", f"B{i + 7}"))
        assert quiet(h.merge, run) == ["M1"]
        t = (R / "findings-1.md").read_text()
        for k, rid in enumerate(RIDS):
            assert f"#### M1.{'abcd'[k]} (round1-{rid}.md B{k + 7})" in t
        assert "Recommendation" not in t and "ARCHITECTURE" not in t and "noise" not in t
        # one lost reviewer: merge over the other three
        st = h.load(run)
        st["merge"], st["r1_lost"] = {}, ["R1.t4-1"]
        h.save(run, st)
        quiet(h.merge, run)
        assert set(h.load(run)["merge"]["reviewers"]) == set(RIDS[:3])


def test_adj_prep_panel_and_full():
    with env():
        quiet(h.build, "sonnet")
        run = "d5-r1"
        put_panel(run, FOUR)
        mids = quiet(h.merge, run)
        p = quiet(h.prep, run, "ADJ")
        st = h.load(run)
        mp = json.load(open(h.run_dir(run) / "adj-map.json"))
        assert sorted(mp.values(), key=lambda m: int(m[1:])) == mids and st["log"]["ADJ"]["map"] == mp
        inp = (h.run_dir(run) / "adj/ws" / h.REVIEW / "adj-input.md").read_text()
        assert inp.startswith("# Findings to adjudicate") and not h.check_findings_text(inp)
        assert not re.search(r"(?m)^#{3,4} M\d", inp) and "round1-t" not in inp                       # blind to merged ids and to reviewer / tier
        assert len(re.findall(r"(?m)^### X\d+$", inp)) == len(mids)
        text = p.read_text()
        assert h.ADJ_BRIEF in text and "COMMAND:" not in text
        assert h.expected_model(st, "ADJ") == "sonnet"
        assert list(mp) == [f"X{i}" for i in range(1, len(mids) + 1)]
        assert quiet(h.prep, run, "ADJ") and json.load(open(h.run_dir(run) / "adj-map.json")) == mp     # deterministic shuffle (Random(run))
        tab, ok = h.parse_adj(adj_reply(mp), mp)
        assert ok and set(tab) == set(mids)
    with env():                                                                  # full variant: PN1 prep_adj over ALL ledger rows
        quiet(h.build, "sonnet", False, "full")
        run = "d5f-r1"
        R = h.ws(run) / h.REVIEW
        for rid, prid in zip(RIDS, PN1_RIDS):
            (R / f"round1-{rid}.md").write_text(fx(f"pn1-b1-r1__round1-{prid}.md").read_text())
        m = full.merge(run, 1)
        led = json.load(open(R / "ledger.json"))
        quiet(h.prep, run, "ADJ")
        mp = json.load(open(h.run_dir(run) / "adj-map.json"))
        assert sorted(mp.values()) == sorted(r["lid"] for r in led["rows"]) and len(mp) > len(m["brief_ids"])
        inp = (h.run_dir(run) / "adj/ws" / h.REVIEW / "adj-input.md").read_text()
        assert "- anchor: " in inp and "- claim: " in inp and "- refs: " in inp


# ------------------------------------------------------------------ VF contamination guard, confirmed line
def test_vf_contamination_guard():
    with env():
        quiet(h.build, "sonnet")
        run = "d5-r1"
        put_panel(run, FOUR)
        quiet(h.merge, run)
        R = h.ws(run) / h.REVIEW
        f1 = R / "findings-1.md"
        f1.write_text(f1.read_text() + "\n=== ARCHITECTURE ANALYSIS ===\n- Recommendation: x\n")
        try:
            quiet(h.prep, run, "VF1")
            raise AssertionError("contaminated VF1 list accepted")
        except ValueError:
            pass
        assert "VF1" not in h.load(run)["prepared"]
        out = adv()                                                              # advance turns it into a MANUAL stop, not a crash / launch
        assert not any("PROMPT-VF1" in ln for ln in launches(out))
        for n, name in ((2, "b1-r6-contaminated__round2.md"), (3, "b1h-r4__round3.md")):
            (R / f"round{n}.md").write_text(fx(name).read_text())
            text, ids = h.findings_text(run, n)
            assert ids and not h.check_findings_text(text)


def test_confirmed_line_authority():
    text = fx("b1h-r3__verify-1.md").read_text()
    ids = [f"M{i}" for i in range(1, 11)]
    table, ok = h.parse_verify(text, ids)
    assert table["M4"][0] == "reject"
    fixed = h.reconcile_confirmed(table, ids, text)
    assert fixed["M4"][0] == "confirm"
    assert [i for i in ids if fixed[i][0] == "confirm"] == ["M3", "M4", "M6", "M7", "M8", "M10"]
    syn = verify_reply(["M1", "M2"], ["M1", "M2"]).replace("confirmed: M1, M2", "confirmed: M1")
    t2, _ = h.parse_verify(syn, ["M1", "M2"])
    assert h.reconcile_confirmed(t2, ["M1", "M2"], syn)["M2"][0] == "reject"
    with env():
        quiet(h.build, "sonnet")
        run = "d5-r1"
        st = h.load(run)
        st["log"]["VF1"] = {"finding_ids": ["M1", "M4"]}
        st["merge"] = {"groups": [{"mid": m, "theme": "other", "cited": [], "heading": "h", "members": []} for m in ("M1", "M4")],
                       "reviewers": {r: {"verdict": "FAIL", "sha256": "0"} for r in RIDS}}
        h.save(run, st)
        outp = h.out_path(run, "VF1")
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text("| id | f | e | o | verdict | reason |\n|---|---|---|---|---|---|\n| M1 | x | yes | yes | confirm | ok |\n"
                        "| M4 | M4.a: x | yes | no | reject | gap |\n| M4 | M4.b: y | yes | yes | confirm | holds |\nconfirmed: M1, M4\n")
        meta = quiet(h.ingest_vf, run, h.load(run), 1, outp)
        assert meta["confirmed"] == ["M1", "M4"] and not meta["rejected"]
        assert "over four independent first reviews" in (h.ws(run) / h.REVIEW / "round1.md").read_text()


# ------------------------------------------------------------------ tokens: pasted, wrapped, short launches, dotted step names, lanes
def write_transcript(path, first_user, msgs, model=SONNET, done=True):
    rows = [{"type": "user", "message": {"role": "user", "content": first_user}}]
    for mid, tokens in msgs:
        for ot in tokens:
            rows.append({"type": "assistant", "message": {"role": "assistant", "id": mid, "model": model, "usage": {"output_tokens": ot},
                                                          "content": [{"type": "text", "text": "x"}]}})
    if done:
        rows.append({"type": "assistant", "message": {"role": "assistant", "id": "last", "model": model, "usage": {"output_tokens": 5},
                                                      "content": [{"type": "text", "text": "DONE /x/round1.md"}]}})
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def test_token_matcher_pasted_and_short_launches():
    with env() as tmp:
        quiet(h.build, "sonnet")
        adv(["--dry-run"])
        tdir = tmp / "tasks"
        tdir.mkdir()
        h.TASKS_GLOB = str(tdir / "*.output")
        rd = h.run_dir("d5-r1")
        pa = (rd / "PROMPT-R1.t1b-1.md").read_text()
        write_transcript(tdir / "a.output", pa, [("m1", [10, 40, 90]), ("m2", [7, 7])])                       # pasted, ids once at max
        write_transcript(tdir / "c.output", "<ctx>\n" + (h.run_dir("d5-r2") / "PROMPT-R1.t2-1.md").read_text() + "\n</ctx>", [("n1", [100])],
                         model=HAIKU)                                                             # wrapped
        write_transcript(tdir / "b.output", f"Read {rd / 'PROMPT-R1.t4-1.md'} and follow it exactly", [("k1", [25, 30])], model=HAIKU)
        write_transcript(tdir / "d.output", f"Read {h.run_dir('d5-r3')}/r1-t3-1/PROMPT.md and follow it exactly", [("q", [3])], model=HAIKU)
        write_transcript(tdir / "z.output", "something else entirely", [("z1", [999])])
        write_transcript(tdir / "w.output", pa, [("w1", [5000])], model=HAIKU)                   # wrong model for t1b-1: ignored
        idx = h.scan_by_prompt()
        assert set(idx) == {("d5-r1", "R1.t1b-1"), ("d5-r2", "R1.t2-1"), ("d5-r1", "R1.t4-1"), ("d5-r3", "R1.t3-1")}, set(idx)
        assert quiet(h.pick, idx[("d5-r1", "R1.t1b-1")], "sonnet")["tokens"] == 102
        assert h.pick(idx[("d5-r2", "R1.t2-1")], "haiku")["tokens"] == 105
        assert h.pick(idx[("d5-r1", "R1.t4-1")], "haiku")["tokens"] == 35
        st = h.load("d5-r1")
        for s in ("R1.t1b-1", "R1.t4-1"):
            st["log"][s] = {"output_exists": True}
        h.save("d5-r1", st)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            h.tokens_cmd("d5-r1")
        st = h.load("d5-r1")
        assert st["log"]["R1.t1b-1"]["output_tokens"] == 102 and st["log"]["R1.t4-1"]["output_tokens"] == 35
        assert st["log"]["R1.t4-1"]["observed_model"] == HAIKU
        assert "loop 137" in buf.getvalue()
        table = h.prompt_table()
        assert h.resolve_short(f"Read {h.run_dir('d5-r3')}/vf2/PROMPT.md and follow it exactly", table) == ("d5-r3", "VF2")
        assert h.resolve_short(f"Read {h.run_dir('d5-r3')}/r2-t1b-1/PROMPT.md and follow it exactly", table) == ("d5-r3", "R2")
        assert h.resolve_short(f"Read {h.run_dir('d5-r4')}/PROMPT-R1.t1b-1.md and follow it exactly", table) == ("d5-r4", "R1.t1b-1")


def test_lanes_from_data_and_ledger_models():
    dec = json.load(open(AB / "decision.json"))
    assert dec["FRESH_LOOP_BASE"] == 53623
    assert h.lane_of("R1.t1b-1", dec) == "primary" and h.lane_of("R1.t4-1", dec) == "tier234" and h.lane_of("ADJ", dec) == "primary"
    assert {h.lane_of(f"R1.{r}", dec) for r in RIDS[1:]} == {"tier234"}
    assert h.lane_of("AUD2", dec) == "audit" and h.lane_of("V2", dec) == "primary" and h.lane_of("XYZ", dec) == "primary"
    assert "Sonnet" in dec["lanes"]["_labels"]["primary"]
    moved = json.loads(json.dumps(dec))
    moved["lanes"]["tier234"]["slots"].remove("t2")
    moved["lanes"]["primary"]["slots"].append("t2")                             # a slot that moves lane is a data change
    assert h.lane_of("R1.t2-1", moved) == "primary" and h.lane_of("R1.t4-1", moved) == "tier234"
    toks = {"R1.t1b-1": 100, "R1.t2-1": 10, "R1.t3-1": 20, "R1.t4-1": 30, "ADJ": 7, "VF1": 5, "V1": 50, "R2": 40, "AUD": 999, "AUD2": 888}
    lt = h.lane_tokens(toks, dec)
    assert lt == {"primary": 202, "tier234": 60, "audit": 1887, "loop": 262, "ADJ": 7,
                  "slots": {"t1b-1": 100, "t2-1": 10, "t3-1": 20, "t4-1": 30}}
    with env() as tmp:
        quiet(h.build, "sonnet")
        st = h.load("d5-r1")
        st["log"]["R1.t2-1"] = {"output_exists": True, "model": "haiku"}
        st["log"]["R1.t1b-1"] = {"output_exists": True, "model": "sonnet", "observed_model": SONNET}
        st["log"]["R1.t3-1"] = {"output_exists": True, "model": "haiku"}
        h.save("d5-r1", st)
        (tmp / "launch-ledger.jsonl").write_text(json.dumps({"run": "d5-r1", "step": "R1.t2-1", "stratum": "sonnet", "model": "haiku-from-ledger"}) + "\n")
        led = h.ledger_models()
        assert h.step_model("d5-r1", st, "R1.t1b-1", led) == SONNET                        # transcript first
        assert h.step_model("d5-r1", st, "R1.t2-1", led) == "haiku-from-ledger"           # then the launch ledger
        assert h.step_model("d5-r1", st, "R1.t3-1", led) == "haiku"                       # then the step record


# ------------------------------------------------------------------ D2 / D6
def test_decision_constants_and_no_cost_kill():
    d = json.load(open(AB / "decision.json"))
    assert (d["A_BASE"], d["AUD_BASE"], d["B_BASE"]) == (100424, 69044, 169468)
    assert round((2.0 * 169468 - 69044) / 100424, 2) == d["rules"]["DROP2_RLOOP_LIMIT"] == 2.69
    assert d["MAX_CONCURRENT_RUNS"] == 6 and d["panel"]["sweep_reviewer"] == "t1b-1"
    src = (AB / "advance.py").read_text() + (AB / "harness.py").read_text() + (AB / "full.py").read_text()
    assert not re.search(r"(?i)abort|TaskStop|kill", src)
    assert "R_LOOP" not in (AB / "advance.py").read_text()


# ------------------------------------------------------------------ whole loops on fixtures, then analyze
def run_audits(run):
    for step in ("AUD", "AUD2"):
        fake(run, step, fx("b1-r4__round1-a.md").read_text())
    for _ in range(4):
        out = adv()
        if h.load(run)["complete"]:
            return out
    raise AssertionError(out)


def test_full_loop_panel_variant_and_analyze():
    with env() as tmp:
        quiet(h.build, "sonnet")
        run = "d5-r1"
        adv()
        for rid, name in zip(RIDS, FOUR):
            fake(run, f"R1.{rid}", fx(name).read_text())
        out = adv()
        assert not any(ln.startswith(("MANUAL", "LOST")) for ln in out.splitlines()), out
        st = h.load(run)
        assert st["merge"]["done"] and {"VF1", "ADJ"} <= set(st["prepared"])
        assert any("PROMPT-VF1.md model=sonnet" in ln for ln in launches(out)) and any("PROMPT-ADJ.md model=sonnet" in ln for ln in launches(out))
        vf1 = (h.run_dir(run) / "PROMPT-VF1.md").read_text()
        assert not h.check_findings_text(vf1[vf1.index("Findings:"):vf1.index("Write your full reply")])
        ids1 = st["log"]["VF1"]["finding_ids"]
        fake(run, "VF1", verify_reply(ids1, ids1[:-1]))
        fake(run, "ADJ", adj_reply(st["log"]["ADJ"]["map"]))
        adv()
        st = h.load(run)
        assert st["log"]["VF1"]["confirmed"] == ids1[:-1] and "V1" in st["prepared"] and st["log"]["ADJ"]["parse_ok"]
        assert not re.search(r"(?m)^={3,}", (h.ws(run) / h.REVIEW / "round1.md").read_text())
        fake(run, "V1", "revise1\n")
        adv()
        assert "R2" in h.load(run)["prepared"] and (h.ws(run) / h.lint_rel(2)).exists()
        fake(run, "R2", fx("b1-r6-contaminated__round2.md").read_text())
        adv()
        st = h.load(run)
        assert st["log"]["VF2"]["finding_ids"] == ["N1", "N2"]
        fake(run, "VF2", verify_reply(["N1", "N2"], ["N1", "N2"]))
        adv()
        fake(run, "V2", "revise2\n")
        adv()
        fake(run, "R3", fx("b1h-r4__round3.md").read_text())
        adv()
        assert h.load(run)["log"]["VF3"]["finding_ids"] == ["N3"]
        fake(run, "VF3", verify_reply(["N3"], []))
        adv()
        st = h.load(run)
        assert st["loop_end"] == "VERIFIED-PASS" and {"AUD", "AUD2"} <= set(st["prepared"])
        assert (h.run_dir(run) / "aud/ws" / h.SPEC).exists()                  # the final spec path the coordinator scores
        run_audits(run)
        st = h.load(run)
        assert st["complete"]
        for s in h.STEPS:
            assert st["log"][s]["stratum"] == "sonnet" and st["log"][s]["model"] in ("sonnet", "haiku"), s
        _tokens_and_analyze(tmp, run, "panel")


def _tokens_and_analyze(tmp, run, variant):
    st = h.load(run)
    for i, s in enumerate(h.STEPS, 1):                                           # tokens as `harness.py tokens` would record them
        st["log"][s]["output_tokens"] = 1000 * i
    h.save(run, st)
    m = quiet(h.analyze)
    res = (tmp / "RESULTS.md").read_text()
    assert "### Lanes" in res and "Headline ratios vs the fresh-baseline loop (53,623 tokens)" in res
    assert "of which ADJ (adjudicator, Sonnet)" in res and "parallel other-provider" in res and "(stand-in)" in res
    for r in RIDS[1:]:
        assert f"{r} live " in res
    assert "Loop-only output tokens per run, by step group" in res and "| merge |" not in res.split("by step group")[0][-5:]
    assert f"/ sonnet" in res or "/ ?" in res
    r = m[variant]["runs"][run]
    lt = r["lane_tokens"]
    tok = {s: 1000 * i for i, s in enumerate(h.STEPS, 1)}
    assert lt["audit"] == tok["AUD"] + tok["AUD2"] and lt["ADJ"] == tok["ADJ"]
    assert lt["tier234"] == tok["R1.t2-1"] + tok["R1.t3-1"] + tok["R1.t4-1"]
    assert lt["loop"] == sum(v for s, v in tok.items() if s not in ("AUD", "AUD2")) == r["loop_tokens_incl_adj"]
    assert m[variant]["lane_headline"]["loop"] == lt["loop"] / 53623
    assert m[variant]["sonnet"]["outcome"] == "INCONCLUSIVE"
    assert r["final_spec_path"].endswith("aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md")
    assert "audit 1 BLK" in res


def test_full_loop_full_variant_and_analyze():
    """variant full: panel -> merge + ledger (M1) -> ADJ (ledger rows) beside VF1 -> V1 -> ledger revise (L1) -> R2 in PN1 sandbox
    (ledger round 2) -> VF2 -> V2 -> L2 -> R3 -> M3 PASS -> AUD/AUD2 -> analyze."""
    with env() as tmp:
        quiet(h.build, "sonnet", False, "full")
        run = "d5f-r1"
        out = adv()
        assert len(launches(out)) == 24 and all("/d5f-r" in ln for ln in launches(out))
        rules = (h.run_dir(run) / "r1-t2-1/home/.claude/rules/prompts/document_review_loop_prompts.md").read_text()
        assert "### Findings block" in rules and rules.count("- **Lint evidence**") == 2
        assert h.SWEEP in (h.run_dir(run) / "PROMPT-R1.t1b-1.md").read_text() and h.SWEEP not in (h.run_dir(run) / "PROMPT-R1.t2-1.md").read_text()
        for rid, prid in zip(RIDS, PN1_RIDS):
            fake(run, f"R1.{rid}", fx(f"pn1-b1-r1__round1-{prid}.md").read_text())
        out = adv()
        assert not any(ln.startswith(("MANUAL", "LOST")) for ln in out.splitlines()), out
        st = h.load(run)
        R = h.ws(run) / h.REVIEW
        m1 = st["log"]["M1"]
        assert m1["decision"] == "REVISE" and m1["brief_ids"] and (R / "ledger.json").exists()
        assert all(st["log"][f"R1.{r}"]["block_ok"] for r in RIDS) and (h.run_dir(run) / "telemetry-R1.t2-1.json").exists()
        assert json.load(open(h.run_dir(run) / "telemetry-R1.t2-1.json"))["slot"]["stand_in"] is True
        round1 = (R / "round1.md").read_text()
        assert round1.startswith("review: 1 of 3") and "## Ledger" in round1
        assert st["log"]["VF1"]["finding_ids"] == m1["brief_ids"] and {"VF1", "ADJ"} <= set(st["prepared"])
        vf1 = (h.run_dir(run) / "PROMPT-VF1.md").read_text()
        assert not h.check_findings_text(vf1[vf1.index("Findings:"):vf1.index("Write your full reply")])
        ids1 = m1["brief_ids"]
        keep, drop = ids1[:2], ids1[2:]
        fake(run, "VF1", verify_reply(ids1, keep))
        fake(run, "ADJ", adj_reply(st["log"]["ADJ"]["map"], "unsure"))
        adv()
        st = h.load(run)
        assert st["log"]["VF1"]["confirmed"] == keep
        led = json.load(open(R / "ledger.json"))
        assert all(r["status"] == "deferred" for r in led["rows"] if r["lid"] in drop)                 # VF-rejected rows are parked
        assert led["rounds"][-1]["brief_ids"] == keep
        assert f"Blocking finding ids: {', '.join(keep)}." in (R / "round1.md").read_text()
        assert f"IDS={', '.join(keep)}" in (h.run_dir(run) / "PROMPT-V1.md").read_text()
        # reviser edits the spec at the first kept row's anchor and returns a fix map
        spec = h.ws(run) / h.SPEC
        row = next(r for r in led["rows"] if r["lid"] == keep[0])
        txt = spec.read_text()
        assert row["anchor"] in txt
        spec.write_text(txt.replace(row["anchor"], row["anchor"] + " (narrowed)", 1))
        fm = "\n".join(json.dumps({"id": i, "action": "applied" if i == keep[0] else "rejected", "reason": "r"}) for i in keep)
        fake(run, "V1", f"bytes\n\n## Fix map\n\n```fixmap-v1\n{fm}\n```\n")
        adv()
        st = h.load(run)
        assert st["log"]["L1"]["resolved_check"] == [keep[0]] and st["log"]["L1"]["fixmap_ok"]
        assert "R2" in st["prepared"]
        sb = h.run_dir(run) / "r2-t1b-1/ws"
        assert (sb / h.HIST / "spec-v1.md").exists() and (sb / h.REVIEW / "round1.md").read_text() == (R / "round1.md").read_text()
        assert (sb / h.lint_rel(2)).exists() and f"lint={h.lint_rel(2)}" in (h.run_dir(run) / "PROMPT-R2.md").read_text()
        assert str(h.run_dir(run) / "r2-t1b-1") in (h.run_dir(run) / "PROMPT-R2.md").read_text()
        # R2: keeps the second kept row open, one new blocking finding
        anchor2 = next(r for r in led["rows"] if r["lid"] == keep[1])["anchor"]
        new_anchor = next(ln for ln in spec.read_text().splitlines() if len(ln) > 60 and ln.strip() not in (row["anchor"], anchor2))[:80]
        blk = [json.dumps({"id": "N1", "severity": "MAJOR", "blocking": True, "category": "contradiction", "anchor": new_anchor, "refs": ["WC-4"], "claim": "new"}),
               json.dumps({"prior": keep[0], "status": "resolved"}), json.dumps({"prior": keep[1], "status": "open"})]
        r2 = f"review: 2 of 3\n\n### N1\ntext\n\n## Reviser brief\n\nBlocking finding ids: N1.\n\nverdict: FAIL\n\n## Findings block\n\n```findings-v1\n" + "\n".join(blk) + "\n```\n"
        fake(run, "R2", r2)
        out = adv()
        assert not any(ln.startswith(("MANUAL", "LOST")) for ln in out.splitlines()), out
        st = h.load(run)
        m2 = st["log"]["M2"]
        assert m2["decision"] == "REVISE" and keep[0] in m2["cleared"] and keep[1] in m2["brief_ids"] and len(m2["new"]) == 1
        assert st["log"]["VF2"]["finding_ids"] == m2["brief_ids"] and (R / "round2-t1b-1.md").exists()
        fake(run, "VF2", verify_reply(m2["brief_ids"], m2["brief_ids"]))
        adv()
        assert "V2" in h.load(run)["prepared"]
        fake(run, "V2", "## Fix map\n\n```fixmap-v1\n" + "\n".join(json.dumps({"id": i, "action": "rejected", "reason": "r"}) for i in m2["brief_ids"]) + "\n```\n")
        adv()
        st = h.load(run)
        assert set(st["log"]["L2"]["rejected"]) == set(m2["brief_ids"]) and "R3" in st["prepared"]
        r3 = "review: 3 of 3\n\nAll resolved.\n\nverdict: PASS\n\n## Findings block\n\n```findings-v1\n" + "\n".join(
            json.dumps({"prior": i, "status": "resolved"}) for i in m2["brief_ids"]) + "\n```\n"
        fake(run, "R3", r3)
        adv()
        st = h.load(run)
        # the ledger, not the reviewer's verdict, decides: rows still open after R3 -> ESCALATE -> VF3 (ab4 cap rule)
        m3 = st["log"]["M3"]
        assert m3["decision"] in ("ESCALATE", "PASS")
        if m3["decision"] == "ESCALATE":
            assert "VF3" in st["prepared"]
            fake(run, "VF3", verify_reply(m3["brief_ids"], []))
            adv()
            st = h.load(run)
            assert st["loop_end"] == "VERIFIED-PASS"
        else:
            assert st["loop_end"] == "PASS"
        run_audits(run)
        st = h.load(run)
        assert st["complete"] and st["variant"] == "full"
        for s in h.STEPS:
            assert st["log"][s]["stratum"] == "sonnet" and st["log"][s]["model"] in ("sonnet", "haiku"), s
        for ln in (tmp / "launch-ledger.jsonl").read_text().splitlines():
            rec = json.loads(ln)
            assert rec["stratum"] == "sonnet" and rec["model"] in ("sonnet", "haiku")
        _tokens_and_analyze(tmp, run, "full")


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
