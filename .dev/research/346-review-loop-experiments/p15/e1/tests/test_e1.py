import copy
import itertools
import json
import pathlib
import re
import shutil

import pytest

import _boot
import analyze_offline as AN
import cases_smoke as CS
import ingest_labels as IL
import policy
import prep_offline as PO
import questions as Q
import replay as RP
from jevlib import config as C
from jevlib.budget import Budget
from jevlib.client import JevClient
from jevlib.journal import Journal
from jevlib.questions import build_request, request_sha256
from jevlib.transport import MockStep, MockTransport, TransportError, TransportTimeout, fake_answer
from p15common import analysis as A
from p15common import datasets
from packets import build_packet, packet_state, sha256_text

E1 = _boot.E1
FAKE_KEY = "TEST-FAKE-KEY-0000000000000000"


# ---------------------------------------------------------------- helpers
@pytest.fixture(scope="module")
def smoke():
    return CS.build_all()


def by(smoke, cat, var):
    return next(c for c in smoke if c["category"] == cat and c["variant"] == var)


def pk_of(case):
    i = case["packet"]["inputs"]
    return build_packet(i["before_text"], i["after_text"], i["finding"], i["history"])


def dec_tmp(tmp_path, usd=5.0, tokens=30_000_000):
    d = RP.load_decision()
    d = copy.deepcopy(d)
    d["jev"]["offline_ceiling_usd"], d["jev"]["offline_ceiling_input_tokens"] = usd, tokens
    return d


def run(tmp_path, smoke, p, transport=None, live=True, **kw):
    t = transport or MockTransport(lambda req: MockStep(200, fake_answer(req, p=p)))
    s = RP.run_replay("smoke", live=live, transport=t, dec=kw.pop("dec", dec_tmp(tmp_path)), cases=smoke,
                      budget_path=tmp_path / "budget.json", journal_dir=tmp_path / "journal", out_dir=tmp_path / "out",
                      sleep=lambda s: None, announce=lambda *a: None, **kw)
    return s, t


# ---------------------------------------------------------------- packets
def test_packet_cited_lines_and_obligation(smoke):
    c = by(smoke, "C1", "v1")
    pk = pk_of(c)
    lines = c["packet"]["inputs"]["before_text"].splitlines()
    assert pk.precheck == "ok" and len(pk.cited) == 2
    assert "**RF-3 " in lines[pk.obligation_lines[0] - 1] and "**RF-4 " in lines[pk.defect_lines[0] - 1]
    assert pk.obligation_text == lines[pk.obligation_lines[0] - 1]            # verbatim before line
    assert pk.obligation_where == f"before, line {pk.obligation_lines[0]}"
    assert pk.wrong_outcome.startswith("An implementer who follows RF-4 builds") and pk.wrong_outcome.endswith(".")
    assert pk.obligation_still_verbatim is True and pk.defect_still_verbatim is False
    assert pk.tombstones == [{"line": pk.defect_lines[0], "text": lines[pk.defect_lines[0] - 1]}]
    assert pk.mapped_hunks == 1 and "-- **RF-4" in pk.diff and "+- **RF-4" in pk.diff
    assert pk.before_sha == sha256_text(c["packet"]["inputs"]["before_text"])


def test_grading_sentence_falls_back_to_heading(smoke):
    i = by(smoke, "C1", "v1")["packet"]["inputs"]
    f = dict(i["finding"]); f["body"] = re.sub(r"An implementer who follows.*\n", "", f["body"])
    pk = build_packet(i["before_text"], i["after_text"], f, i["history"])
    assert pk.wrong_outcome == "R1-1 Refund method forces store credit"


def test_obligation_without_marker_uses_first_cited_line_on_contradiction():
    before = "# T\n\n- **AA-1 One.** Always do x.\n- **AA-2 Two.** Never do x.\n\n- **AA-3 Three.** Other.\n"
    after = before.replace("Never do x.", "Do x on request.")
    f = {"run": "r", "review": "R1", "id": "R1-1", "heading": "### R1-1 conflict", "body": "AA-1 and AA-2 contradict each other (lines 3-4 of the spec).\nAn implementer who follows AA-2 builds x."}
    pk = build_packet(before, after, f, {})
    assert pk.obligation_lines == [3] and pk.defect_lines == [4]


def test_noop_whitespace_is_open_without_call(tmp_path, smoke):
    c = by(smoke, "C2", "v1")
    pk = pk_of(c)
    assert pk.precheck == "noop" and not pk.eligible
    assert policy.decide(pk.precheck, None, policy.DEFAULT_THR) == policy.OPEN
    s, t = run(tmp_path, smoke, 0.5)
    rows = [json.loads(x) for x in (tmp_path / "out/replay-smoke.jsonl").read_text().splitlines()]
    r = next(x for x in rows if x["case_id"] == c["case_id"])
    assert r["decision"] == policy.OPEN and r["status"] == "not_called"
    called = {json.loads(x)["case_id"] for x in (tmp_path / "journal/jev-smoke.jsonl").read_text().splitlines()}
    noops = {x["case_id"] for x in rows if x["precheck"] == "noop"}
    assert noops and c["case_id"] in noops and not (called & noops)        # no request was made for a no-op packet
    assert len(t.calls) == sum(1 for c in smoke if c["packet"]["precheck"] == "ok")


def test_stale_unmapped_oversize_not_eligible(smoke):
    c = by(smoke, "C1", "v1")
    i = c["packet"]["inputs"]
    stale = build_packet(i["before_text"], i["after_text"], i["finding"], {"recorded_before_sha": "0" * 64})
    assert stale.precheck == "stale"
    f = dict(i["finding"]); f["body"] = "No line is cited here.\nAn implementer who follows X builds Y."; f["heading"] = "### R1-1 nothing"
    unm = build_packet(i["before_text"], i["after_text"], f, {})
    assert unm.precheck == "unmapped"
    f2 = dict(i["finding"]); f2["body"] = "Cited: spec lines 900 (before version).\nAn implementer who follows X builds Y."
    assert build_packet(i["before_text"], i["after_text"], f2, {}).precheck == "unmapped"      # line beyond the document
    big = "\n".join(f"- **BB-{n} Filler.** " + "word " * 40 for n in range(1000))
    before = "# T\n\n- **AA-1 Rule.** The cap is ten.\n" + big + "\n"
    huge = "\n".join(f"- **CC-{n} Other.** " + "text " * 40 for n in range(1500))
    after = before.replace("The cap is ten.", "The cap is twelve.\n" + huge)                 # a huge changed region
    f3 = {"run": "r", "review": "R1", "id": "R1-1", "heading": "### R1-1 cap", "body": "Cited: spec lines 3 (before version).\nAn implementer who follows AA-1 builds a cap of ten."}
    over = build_packet(before, after, f3, {})
    assert over.precheck == "oversize" and not over.eligible
    deps = pk_of(by(smoke, "C10", "v1"))
    assert deps.precheck == "deps" and deps.n_deps_needed == 4
    for pre in ("stale", "unmapped", "oversize", "deps"):
        assert policy.decide(pre, None, policy.DEFAULT_THR) == policy.NOT_ELIGIBLE


def test_regressed_previously_closed_is_open():
    before = "# T\n\n- **AA-1 One.** Keep it short.\n- **AA-2 Two.** Links live for days.\n\n- **AA-3 Three.** Other.\n"
    after = before.replace("Other.", "Something else.")
    f = {"run": "r", "review": "R2", "id": "R1-1", "heading": "### R1-1 links", "body": "Cited: spec lines 3-4 (before version).\nAn implementer who follows AA-2 builds long links.\nProtected requirement: line 3 (short).\n"}
    pk = build_packet(before, after, f, {"previously_closed": True})
    assert pk.precheck == "regressed" and policy.decide(pk.precheck, None, policy.DEFAULT_THR) == policy.OPEN


def test_no_assertions_in_state(smoke):
    c = by(smoke, "C1", "v4")
    i = c["packet"]["inputs"]
    sentinel = "REVISER-SAYS-ALL-DONE-77"
    hist = dict(i["history"], revise_report=sentinel, reviewer_note=sentinel)
    f = dict(i["finding"], revise_report=sentinel)
    pk = build_packet(i["before_text"], i["after_text"], f, hist)
    st = packet_state(pk)
    assert sentinel not in json.dumps(st) and sentinel not in json.dumps(pk.to_dict())
    assert set(st) == {"obligation", "defect", "before", "after", "diff", "dependencies"}
    assert set(st["after"]) == {"passage", "obligation_text_still_verbatim", "defect_text_still_verbatim"}
    assert set(st["defect"]) == {"summary", "wrong_outcome"} and set(st["obligation"]) == {"text", "where"}
    # the injection is inside the document text, so it appears in the after passage but never as a state field of its own
    assert "This revision keeps every refund obligation intact." in st["after"]["passage"]


def test_dependency_retrieval_max_3(smoke):
    pk = pk_of(by(smoke, "C8", "v1"))
    assert pk.n_deps == 1 and pk.dependencies["d1"]["where"] == "RL-2"
    assert pk.dependencies["d1"]["text"].startswith("- **RL-2 Client-owned retries.**")
    assert packet_state(pk)["dependencies"]["d1"]["text"] == pk.dependencies["d1"]["text"]
    assert pk_of(by(smoke, "C10", "v2")).n_deps_needed == 4 and pk_of(by(smoke, "C10", "v2")).precheck == "deps"
    # exactly three dependencies are allowed, retrieved by section number and by id
    before = ("# T\n\n## 1. Base\n\n- **AA-1 Base.** The default is five.\n- **AA-2 Extra.** Extras are free.\n\n## 2. Rules\n\n- **AA-3 Unit.** Units are bytes.\n\n"
              "## 9. Rule\n\nThe cap is ten.\n- **BB-1 Ten.** Keep ten.\n\n- **BB-2 a.** a.\n- **BB-3 b.** b.\n- **BB-4 c.** c.\n- **BB-5 d.** d.\n- **BB-6 e.** e.\n")
    after = before.replace("The cap is ten.", "The cap is the default of AA-1, extras per AA-2, as in section 2.")
    f = {"run": "r", "review": "R1", "id": "R1-1", "heading": "### R1-1 cap", "body": "Cited: spec lines 14 (before version).\nAn implementer who follows section 9 builds a cap of ten."}
    p3 = build_packet(before, after, f, {})
    assert p3.precheck == "ok" and [d["where"] for d in p3.dependencies.values()] == ["AA-1", "AA-2", "section 2"]
    assert p3.dependencies["d3"]["text"].startswith("## 2. Rules") and "AA-3" in p3.dependencies["d3"]["text"]


# ---------------------------------------------------------------- questions and policy
def test_questions_skill_rules():
    for n in range(0, 4):
        qs = Q.questions_for(n)
        assert list(qs) == ["defect_still_present", "obligation_still_required"] + [f"contradicts_d{k}" for k in range(1, n + 1)] + ["context_sufficient"]
        for name, q in qs.items():
            assert re.match(C.QNAME_RE, name)
            assert q["type"] == "noul" and set(q["criteria"]) == {"true", "false"}
            assert all(q["criteria"].values()) and q["instructions"].strip().endswith("?")
            assert " or " not in q["instructions"] and " and " not in q["instructions"], name        # one judgment per question
        build_request({"a": 1}, qs)                                                                    # builds for the contract
    with pytest.raises(ValueError):
        Q.questions_for(4)
    assert Q.QSET_VERSION == "e1-q1"
    assert Q.questions_for(2)["contradicts_d2"]["instructions"] == "Does `after.passage` contradict `dependencies.d2.text`?"


def _ans(present, obl, ctx, contra=()):
    a = {"defect_still_present": {"type": "noul", "p": present}, "obligation_still_required": {"type": "noul", "p": obl},
         "context_sufficient": {"type": "noul", "p": ctx}}
    for k, p in enumerate(contra, 1):
        a[f"contradicts_d{k}"] = {"type": "noul", "p": p}
    return a


class R:
    def __init__(self, status="ok", answers=None):
        self.status, self.answers = status, answers


def test_policy_exhaustive_bands():
    thr = policy.DEFAULT_THR
    reps = {"low": 0.0, "mid": 0.5, "high": 1.0}
    for n in range(0, 4):
        closing = 0
        for bands in itertools.product(reps, repeat=3 + n):
            present, obl, ctx, *contra = [reps[b] for b in bands]
            d = policy.decide("ok", R("ok", _ans(present, obl, ctx, contra)), thr, n)
            assert d in (policy.AUTO_CLOSE, policy.FALLBACK)                        # exactly one decision per combination
            expect = bands[0] == "low" and bands[1] == "high" and bands[2] == "high" and all(b == "low" for b in bands[3:])
            assert (d == policy.AUTO_CLOSE) == expect, bands
            closing += d == policy.AUTO_CLOSE
        assert closing == 1                                                          # only the single row of the table closes
    # threshold edges: p < low, p >= high
    assert policy.decide("ok", R("ok", _ans(0.29, 0.7, 0.7)), thr) == policy.AUTO_CLOSE
    assert policy.decide("ok", R("ok", _ans(0.3, 0.7, 0.7)), thr) == policy.FALLBACK
    assert policy.decide("ok", R("ok", _ans(0.1, 0.69, 0.7)), thr) == policy.FALLBACK
    assert policy.decide("ok", R("ok", _ans(0.1, 0.7, 0.69)), thr) == policy.FALLBACK
    assert policy.decide("ok", R("ok", _ans(0.1, 0.9, 0.9, [0.3])), thr, 1) == policy.FALLBACK
    assert policy.decide("noop", None, thr) == policy.OPEN
    for pre in ("stale", "unmapped", "oversize", "deps"):
        assert policy.decide(pre, R("ok", _ans(0, 1, 1)), thr) == policy.NOT_ELIGIBLE
    # a missing answer is never a close
    a = _ans(0.0, 1.0, 1.0); del a["context_sufficient"]
    assert policy.decide("ok", R("ok", a), thr) == policy.FALLBACK
    assert policy.decide("ok", R("ok", _ans(0.0, 1.0, 1.0)), thr, 1) == policy.FALLBACK   # a dependency question without an answer


def test_non_ok_status_never_auto_closes():
    best = _ans(0.0, 1.0, 1.0)
    for status in ("invalid", "unavailable", "refused"):
        for err in ("http_429", "timeout", "model_mismatch", "prob_sum", "oversize", "privacy", "budget_exhausted", "dry_run", "key"):
            assert policy.decide("ok", R(status, best), policy.DEFAULT_THR) == policy.FALLBACK
    assert policy.decide("ok", None, policy.DEFAULT_THR) == policy.FALLBACK


def test_conventional_same_table():
    thr = policy.DEFAULT_THR
    good = {"defect_still_present": "no", "obligation_still_required": "yes", "context_sufficient": "yes"}
    assert policy.conventional_decide("ok", good, thr) == policy.AUTO_CLOSE
    for k, v in (("defect_still_present", "uncertain"), ("defect_still_present", "yes"), ("obligation_still_required", "uncertain"),
                 ("obligation_still_required", "no"), ("context_sufficient", "uncertain"), ("context_sufficient", "no")):
        assert policy.conventional_decide("ok", {**good, k: v}, thr) == policy.OPEN           # OPEN replaces FALLBACK
    assert policy.conventional_decide("ok", {**good, "contradicts_d1": "no"}, thr, 1) == policy.AUTO_CLOSE
    assert policy.conventional_decide("ok", {**good, "contradicts_d1": "uncertain"}, thr, 1) == policy.OPEN
    assert policy.conventional_decide("ok", good, thr, 1) == policy.OPEN                      # missing contradicts answer = uncertain
    assert policy.conventional_decide("ok", {**good, "defect_still_present": "maybe"}, thr) == policy.OPEN
    assert policy.conventional_decide("noop", {}, thr) == policy.OPEN
    assert policy.conventional_decide("deps", {}, thr) == policy.NOT_ELIGIBLE
    # equivalent to the Jev table when yes/no/uncertain are mapped to 1.0/0.0/0.5
    for combo in itertools.product(("yes", "no", "uncertain"), repeat=3):
        ans = dict(zip(("defect_still_present", "obligation_still_required", "context_sufficient"), combo))
        p = {k: {"type": "noul", "p": policy.YES_NO_P[v]} for k, v in ans.items()}
        j = policy.decide("ok", R("ok", p), thr)
        assert (policy.conventional_decide("ok", ans, thr) == policy.AUTO_CLOSE) == (j == policy.AUTO_CLOSE)


# ---------------------------------------------------------------- replay
def test_replay_dry_run_preflight_and_reservation(tmp_path, smoke):
    # dry run: no network object, no call, a pre-flight summary, rows are written apart from the live file
    s, _ = run(tmp_path / "d", smoke, 0.5, live=False)
    assert s["requests"] == 34 and s["reservation_input_tokens"] > 0 and not s["drift"]
    assert s["dry_status"] == {"refused/dry_run": 34}
    assert (tmp_path / "d/out/replay-smoke.dry.jsonl").exists() and not (tmp_path / "d/out/replay-smoke.jsonl").exists()
    # live: the reservation exists before the first call
    seen = {}

    def script(req):
        if "first" not in seen:
            led = json.loads((tmp_path / "l/budget.json").read_text())
            seen["first"] = dict(led["reserved"])
        return MockStep(200, fake_answer(req, p=0.5))
    s2, t = run(tmp_path / "l", smoke, 0.5, transport=MockTransport(script))
    assert "smoke" in seen["first"] and seen["first"]["smoke"]["tokens"] == s2["reservation_input_tokens"]
    assert len(t.calls) == 34 and s2["status_counts"].get("ok") == 34 and "smoke" not in json.loads((tmp_path / "l/budget.json").read_text())["reserved"]
    # estimate over the ceiling: refuses to start, writes BLOCKED-BUDGET, makes no call
    s3, t3 = run(tmp_path / "b", smoke, 0.5, dec=dec_tmp(tmp_path, usd=0.0001, tokens=1000))
    assert s3.get("blocked_budget") is True and t3.calls == []
    blk = json.loads((tmp_path / "b/out/BLOCKED-BUDGET-smoke.json").read_text())
    assert blk["status"] == "BLOCKED-BUDGET" and blk["estimate_input_tokens"] == s3["reservation_input_tokens"]
    assert not (tmp_path / "b/out/replay-smoke.jsonl").exists()


def test_key_missing_is_a_hard_error_never_a_fallback(tmp_path, smoke, monkeypatch):
    monkeypatch.delenv("JEV_API_KEY", raising=False)
    from jevlib.client import KeyMissing
    with pytest.raises(KeyMissing):
        RP.run_replay("smoke", live=True, dec=dec_tmp(tmp_path), cases=smoke, budget_path=tmp_path / "b.json", journal_dir=tmp_path / "j",
                      out_dir=tmp_path / "o", announce=lambda *a: None, transport=MockTransport([]))


@pytest.fixture(autouse=True)
def _key(monkeypatch):
    monkeypatch.setenv("JEV_API_KEY", FAKE_KEY)


def _one(tmp_path, steps, case_cat="C1", var="v1", smoke=None):
    c = by(smoke, case_cat, var)
    pk = pk_of(c)
    st = packet_state(pk)
    sleeps = []
    cl = JevClient(experiment="E1", phase="smoke", budget=Budget(tmp_path / "b.json", ceiling_usd=5.0, ceiling_input_tokens=30_000_000),
                   journal=Journal(tmp_path / "j.jsonl"), transport=MockTransport(steps), live=True, sleep=sleeps.append)
    cl.budget.reserve_phase("smoke", 100000)
    r = cl.ask(st, Q.questions_for(pk.n_deps), case_id=c["case_id"], qset_version=Q.QSET_VERSION, data_classes={"synthetic"}, purpose="t")
    return r, pk


def test_mock_failure_suite(tmp_path, smoke):
    thr = policy.DEFAULT_THR

    def good_body(req):
        return fake_answer(req, p=0.0) | {}

    def decisive(req):    # a perfect closing answer for the packet, used to prove the failure cases do not close by accident
        b = fake_answer(req, p=0.5)
        for k, v in b["answers"].items():
            v["noul"] = {"defect_still_present": 0.0, "obligation_still_required": 1.0, "context_sufficient": 1.0}.get(k, 0.0)
        return b
    scenarios = {
        "timeouts": [MockStep(exc=TransportTimeout("t")), MockStep(exc=TransportTimeout("t"))],
        "transport reset": [MockStep(exc=TransportError("reset")), MockStep(exc=TransportError("reset"))],
        "429 twice": [MockStep(429), MockStep(429)],
        "529 twice": [MockStep(529), MockStep(529)],
        "500 twice": [MockStep(500), MockStep(500)],
        "malformed json": [MockStep(200, b"{not json")],
        "empty object": [MockStep(200, {})],
        "400 oversize": [MockStep(400, b'{"error":"max_tokens_exceeded"}')],
        "422": [MockStep(422, b"{}")],
    }
    for name, steps in scenarios.items():
        r, pk = _one(tmp_path / name.replace(" ", "_"), steps, smoke=smoke)
        assert r.status != "ok", name
        assert policy.decide("ok", r, thr, pk.n_deps) == policy.FALLBACK, name
    # response-level defects on an otherwise closing answer: missing answer, unknown type, alias drift, missing usage
    def mutate(f):
        def script(req):
            b = decisive(req); f(b); return MockStep(200, b)
        return script
    broken = {
        "missing answer": lambda b: b["answers"].pop("context_sufficient"),
        "unknown type": lambda b: b["answers"].__setitem__("context_sufficient", {"type": "score", "score": 1}),
        "model alias drift": lambda b: b.__setitem__("model", "jev-latest"),
        "missing usage": lambda b: b.pop("usage"),
        "noul out of range": lambda b: b["answers"]["defect_still_present"].__setitem__("noul", 1.5),
        "extra answer": lambda b: b["answers"].__setitem__("surprise", {"type": "noul", "noul": 0.0}),
    }
    for name, f in broken.items():
        r, pk = _one(tmp_path / ("x_" + name.replace(" ", "_")), mutate(f), smoke=smoke)
        assert r.status == "invalid" and r.answers is None, name
        assert policy.decide("ok", r, thr, pk.n_deps) == policy.FALLBACK, name
    # 429 then success is retried exactly once and, with an undecided answer, still falls back
    t_steps = [MockStep(429), MockStep(200, fake_answer({"questions": Q.questions_for(0)}, p=0.5))]
    r, pk = _one(tmp_path / "retry", t_steps, smoke=smoke)
    assert r.status == "ok" and r.attempts == 2
    assert policy.decide("ok", r, thr, 0) == policy.FALLBACK
    # control: the decisive answer does close, so the suite above is not passing vacuously
    r, pk = _one(tmp_path / "control", lambda req: MockStep(200, decisive(req)), smoke=smoke)
    assert r.status == "ok" and policy.decide("ok", r, thr, 0) == policy.AUTO_CLOSE
    # oversize is refused locally, without a call
    big = {"x": "word " * 80_000}      # spaces: the jevlib email regex is quadratic on one very long alphanumeric run (reported to the coordinator)
    cl = JevClient(experiment="E1", phase="smoke", budget=Budget(tmp_path / "ob.json", ceiling_usd=5, ceiling_input_tokens=3_000_000),
                   journal=Journal(tmp_path / "oj.jsonl"), transport=MockTransport([]), live=True)
    r = cl.ask(big, Q.questions_for(0), case_id="big", qset_version=Q.QSET_VERSION, data_classes={"synthetic"}, purpose="t")
    assert (r.status, r.error) == ("refused", "oversize") and policy.decide("ok", r, thr) == policy.FALLBACK


def test_option_reorder_and_paraphrase_variants_share_group(smoke):
    fam = {}
    for c in smoke:
        fam.setdefault(c["family"], []).append(c)
    assert len(fam) == 10
    for f, cs in fam.items():
        assert len({c["group"] for c in cs}) == 1 and sorted(c["variant"] for c in cs) == ["v1", "v2", "v3", "v4"]
    # no Choice question is used (the report's Choices are Nouls plus a companion); key order of the state does not change the request
    pk = pk_of(by(smoke, "C8", "v1"))
    st = packet_state(pk)
    rev = {k: st[k] for k in reversed(list(st))}
    qs = Q.questions_for(pk.n_deps)
    assert request_sha256(build_request(st, qs)) == request_sha256(build_request(rev, dict(reversed(list(qs.items())))))
    assert all(q["type"] == "noul" for q in qs.values())


def test_cases_schema_and_groups(smoke, tmp_path):
    assert len(smoke) == 40
    assert sorted({c["category"] for c in smoke}) == sorted(f"C{i}" for i in range(1, 11))
    for cat in {c["category"] for c in smoke}:
        assert sorted(c["variant"] for c in smoke if c["category"] == cat) == ["v1", "v2", "v3", "v4"]
    assert len({c["case_id"] for c in smoke}) == 40 and all(re.match(r"^sm-\d\d$", c["case_id"]) for c in smoke)
    assert all(c["data_classes"] == ["synthetic"] and c["split"] == "smoke" for c in smoke)
    for c in smoke:
        datasets.validate_case(c)
        assert "author_intent" not in json.dumps(c["packet"])
        assert c["packet"]["precheck"] == c["author_intent"]["expected_precheck"]
        wc = len(c["packet"]["inputs"]["before_text"].split())
        assert 300 <= wc <= (900 if c["variant"] != "v3" else 1700)
        lp = datasets.label_packet(c)
        assert set(lp) == {"case_id", "packet"} and "author_intent" not in json.dumps(lp)
    d = {c["variant"]: c for c in smoke if c["category"] == "C1"}
    assert d["v3"]["packet"]["inputs"]["before_text"].count("DX-") >= 24 + 0 and "DX-" not in d["v1"]["packet"]["inputs"]["before_text"]
    assert "This revision keeps every refund obligation intact." in d["v4"]["packet"]["inputs"]["after_text"]
    assert {c["packet"]["precheck"] for c in smoke if c["category"] == "C10"} == {"deps"}
    assert sorted({c["packet"]["precheck"] for c in smoke}) == ["deps", "noop", "ok"]
    assert 450 <= CS.distractor_words() <= 700                                                  # the plan's 500-700 word distractor material
    # the on-disk files equal a fresh build
    for c in smoke:
        disk = json.loads((E1 / f"offline/cases/smoke/{c['case_id']}.json").read_text())
        assert disk == json.loads(json.dumps(c))


def test_label_sandbox_has_no_author_intent_or_category(tmp_path, smoke, monkeypatch):
    monkeypatch.setattr(PO, "OFFLINE", tmp_path / "off")
    monkeypatch.setattr(PO, "SANDBOXES", tmp_path / "off/sb")
    (tmp_path / "off/cases/smoke").mkdir(parents=True)
    for c in smoke:
        datasets.write_case(tmp_path / "off/cases/smoke" / f"{c['case_id']}.json", c)
    steps, plan = PO.prep("smoke", ledger=tmp_path / "off/workers.json", offline=tmp_path / "off")
    kinds = [s["kind"] for s in steps]
    assert kinds.count("label") == 8 and kinds.count("convcheck") == 4
    assert {s["model"] for s in steps if s["id"].startswith("L1")} == {"sonnet"} and {s["model"] for s in steps if s["id"].startswith("L2")} == {"haiku"}
    assert sum(len(v) for v in plan["label_batches"].values()) == 40 and all(len(v) == 10 for v in plan["label_batches"].values())
    assert sum(len(v) for v in plan["conv_batches"].values()) == 34
    # same shuffle for both labelers, shuffled across groups
    assert plan["label_batches"] == PO.prep("smoke", ledger=tmp_path / "off/workers2.json", offline=tmp_path / "off")[1]["label_batches"]
    forbidden = ["author_intent", "expected_precheck", "expect_auto_close", "category_name", "G-refunds", "closure_correct\": \"yes\", \"expected"]
    seen = 0
    for f in (tmp_path / "off/sb").rglob("*"):
        if f.is_file() and f.suffix in (".md", ".json"):
            seen += 1
            txt = f.read_text()
            assert not any(w in txt for w in forbidden), f
            assert not re.search(r"\bC(10|[1-9])\b", txt) or f.name in ("before.md", "after.md"), f
    assert seen > 100
    for s in steps:
        p = pathlib.Path(s["prompt"]).read_text()
        assert "SANDBOX: work ONLY inside" in p and s["out"] in p and "DONE" in p
    cc = next(s for s in steps if s["kind"] == "convcheck")
    txt = pathlib.Path(cc["prompt"]).read_text()
    assert Q.CHECKER_BRIEF_TEXT in txt and "defect_still_present" in txt and "contradicts_dK" in txt
    pkts = json.loads((pathlib.Path(cc["prompt"]).parent / "packets.json").read_text())
    assert all(p["state"] and "dependencies" in p["state"] for p in pkts)
    assert not any("author_intent" in json.dumps(p) for p in pkts)
    # a started step keeps its sandbox when prep is run again
    led = json.loads((tmp_path / "off/workers.json").read_text())
    led["steps"][0]["status"] = "launched"
    (tmp_path / "off/workers.json").write_text(json.dumps(led))
    keep = pathlib.Path(led["steps"][0]["out"]); keep.write_text("x")
    PO.prep("smoke", ledger=tmp_path / "off/workers.json", offline=tmp_path / "off")
    assert keep.read_text() == "x"


def test_label_normalization_and_ingest_rules():
    n = IL.normalize({"case_id": "a", "resolved": "Yes", "obligation_preserved": "n/a", "new_conflict": "no", "closure_correct": "yes", "evidence": "q", "confidence": "high"})
    assert n["closure_correct"] == "yes" and n["confidence"] == "high"
    bad = IL.normalize({"case_id": "a", "resolved": "yes", "obligation_preserved": "yes", "new_conflict": "no", "closure_correct": "no"})
    assert bad["closure_correct"] == "yes" and bad["confidence"] == "low" and bad["inconsistent_closure"]    # derived, flagged
    assert IL.normalize({"case_id": "a", "resolved": "maybe", "obligation_preserved": "yes", "new_conflict": "no"}) is None
    assert IL.normalize({"case_id": "a", "resolved": "undecidable", "obligation_preserved": "yes", "new_conflict": "no"}) is None
    assert IL.normalize({"case_id": "a", "resolved": "undecidable", "obligation_preserved": "yes", "new_conflict": "no"}, True)["closure_correct"] == "undecidable"
    assert IL.derive_closure({"resolved": "yes", "obligation_preserved": "no", "new_conflict": "no"}) == "no"
    assert IL.derive_closure({"resolved": "yes", "obligation_preserved": "yes", "new_conflict": "yes"}) == "no"


# ---------------------------------------------------------------- analysis
def row(cid, decision, truth_group="g", status="ok", precheck="ok", error=None, variant="v1", n_deps=0, cat="C1"):
    return {"case_id": cid, "group": truth_group, "family": truth_group, "category": cat, "variant": variant, "split": "smoke", "precheck": precheck,
            "n_deps": n_deps, "status": status if precheck == "ok" else "not_called", "error": error, "decision": decision, "live": True,
            "answers": {}, "input_tokens": 100, "model": "jev-1.14.0", "latency_ms": 100 + len(cid)}


def truth_of(**kw):
    return {c: {"case_id": c, "closure_correct": v} for c, v in kw.items()}


def test_analysis_false_closure_stop_rule():
    dec = A.load_decision(E1 / "decision.toml")
    ok_rows = [row("a", policy.AUTO_CLOSE), row("b", policy.FALLBACK), row("c", policy.FALLBACK)]
    m = AN.smoke_metrics(ok_rows, truth_of(a="yes", b="no", c="no"))
    assert AN.smoke_verdict(m, dec)[0] == "GO" and m["automation_coverage"] == pytest.approx(1 / 3) and m["true_closures"] == ["a"]
    bad = [row("a", policy.AUTO_CLOSE), row("b", policy.AUTO_CLOSE), row("c", policy.FALLBACK)]
    m = AN.smoke_metrics(bad, truth_of(a="yes", b="no", c="no"))
    v, rule = AN.smoke_verdict(m, dec)
    assert v == "NO-GO-OFFLINE" and m["false_closures"] == ["b"] and "['b']" in rule          # one is enough
    # undecidable truth is excluded from the false-closure count
    m = AN.smoke_metrics(bad, truth_of(a="yes", b="undecidable", c="no"))
    assert m["false_closures"] == [] and AN.smoke_verdict(m, dec)[0] == "BLOCKED"           # an AUTO_CLOSE without decided truth is not trusted
    # BLOCKED: model mismatch; > 10% invalid/unavailable
    mm = [row("a", policy.FALLBACK, status="invalid", error="model_mismatch")] + [row(f"x{i}", policy.FALLBACK) for i in range(9)]
    assert AN.smoke_verdict(AN.smoke_metrics(mm, truth_of(a="no")), dec)[0] == "BLOCKED"
    many = [row(f"i{i}", policy.FALLBACK, status="unavailable", error="http_529") for i in range(2)] + [row(f"x{i}", policy.FALLBACK) for i in range(8)]
    assert AN.smoke_verdict(AN.smoke_metrics(many, {}), dec)[0] == "BLOCKED"
    edge = [row("i0", policy.FALLBACK, status="unavailable", error="http_529")] + [row(f"x{i}", policy.FALLBACK) for i in range(9)]
    assert AN.smoke_verdict(AN.smoke_metrics(edge, {}), dec)[0] == "GO"                       # exactly 10% is not more than 10%
    # a false closure outranks infrastructure trouble
    both = bad + [row("m", policy.FALLBACK, status="invalid", error="model_mismatch")]
    assert AN.smoke_verdict(AN.smoke_metrics(both, truth_of(a="yes", b="no", c="no")), dec)[0] == "NO-GO-OFFLINE"
    # information metrics: conventional agreement and perturbation consistency
    rows = [row("a", policy.AUTO_CLOSE, "g1", variant="v1"), row("b", policy.AUTO_CLOSE, "g1", variant="v2"),
            row("c", policy.FALLBACK, "g2", variant="v1"), row("d", policy.AUTO_CLOSE, "g2", variant="v2")]
    conv = {"a": {"packet_id": "a", "defect_still_present": "no", "obligation_still_required": "yes", "context_sufficient": "yes"},
            "c": {"packet_id": "c", "defect_still_present": "no", "obligation_still_required": "yes", "context_sufficient": "yes"}}
    m = AN.smoke_metrics(rows, truth_of(a="yes", b="yes", c="yes", d="yes"), conv)
    assert m["perturbation_consistent_exact"] == 1 and m["perturbation_consistent_closing"] == 1 and m["conventional_agreement"] == 0.5
    assert m["conventional_false_closures"] == []


def test_cost_reduction_uses_apportioned_checker_tokens():
    plan = {"conv_batches": {"b01": ["a", "b"], "b02": ["c", "d"]}}
    rows = [row("a", policy.AUTO_CLOSE), row("b", policy.FALLBACK), row("c", policy.AUTO_CLOSE), row("d", policy.AUTO_CLOSE)]
    cr = AN.cost_reduction(rows, {"b01": 1000, "b02": 3000}, plan)
    assert cr["tokens_all_eligible"] == 4000 and cr["tokens_fallback"] == 500 and cr["reduction"] == pytest.approx(0.875)
    assert AN.cost_reduction(rows, {}, plan) is None


def test_heldout_gates():
    dec = A.load_decision(E1 / "decision.toml")
    rows = [row(f"c{i}", policy.AUTO_CLOSE if i < 4 else policy.FALLBACK, f"g{i % 3}", cat="C1") for i in range(10)]
    truth = truth_of(**{f"c{i}": ("yes" if i < 4 else "no") for i in range(10)})
    plan = {"conv_batches": {"b01": [f"c{i}" for i in range(10)]}}
    m = AN.heldout_metrics(rows, truth, {}, policy.DEFAULT_THR, {"b01": 10000}, plan)
    v, rule = AN.heldout_verdict(m, dec)
    assert v == "GO-E4" and m["upper_bound_95"] == pytest.approx(3 / 4) and m["conditional_error"] == 0
    rows[4]["decision"] = policy.AUTO_CLOSE                                                      # a false AUTO_CLOSE
    m = AN.heldout_metrics(rows, truth, {}, policy.DEFAULT_THR, {"b01": 10000}, plan)
    assert AN.heldout_verdict(m, dec)[0] == "NO-GO-OFFLINE" and "(a)" in AN.heldout_verdict(m, dec)[1]
    rows[4]["decision"] = policy.FALLBACK
    rows[0]["status"] = "unavailable"                                                            # non-ok status that closed
    m = AN.heldout_metrics(rows, truth, {}, policy.DEFAULT_THR, {"b01": 10000}, plan)
    assert "(e)" in AN.heldout_verdict(m, dec)[1]


def test_results_json_schema(tmp_path):
    dec_path = E1 / "decision.toml"
    rows = [row("a", policy.AUTO_CLOSE), row("b", policy.FALLBACK)]
    base = AN.smoke_metrics(rows, truth_of(a="yes", b="no"))
    bad = AN.smoke_metrics([row("a", policy.AUTO_CLOSE), row("b", policy.AUTO_CLOSE)], truth_of(a="yes", b="no"))
    blocked = AN.smoke_metrics([row("a", policy.FALLBACK, status="invalid", error="model_mismatch")], {})
    dec = A.load_decision(dec_path)
    for name, m, expect in (("go", base, ("PENDING", "PENDING")), ("nogo", bad, ("NO-GO-OFFLINE", "BLOCKED")), ("blocked", blocked, ("BLOCKED", "BLOCKED"))):
        v, rule = AN.smoke_verdict(m, dec)
        res = AN.results_doc("smoke", v, rule, m, dec_path)
        assert A._validate_results(res) == [], name
        assert [r["verdict"] for r in res["rows"]][0] == expect[0] and res["rows"][1]["verdict"] == expect[1] and res["rows"][2]["verdict"] == expect[1]
        assert [r["arm"] for r in res["rows"]] == ["e1-smoke", "f4b", "f4c"]
        assert res["rows"][0]["stratum"] == "offline" and res["rows"][0]["role"] == "offline-gate"
        assert (len(res["blocked_downstream"]) == 1) == (v != "GO")
        A.write_results(tmp_path / f"{name}.json", res)
        assert json.loads((tmp_path / f"{name}.json").read_text())["schema"] == "p15-results/1"
    assert set(A.METRIC_KEYS) <= set(AN.results_doc("smoke", "GO", "r", base, dec_path)["rows"][0]["metrics"])


def test_analyze_cli_end_to_end_without_matrix(tmp_path, smoke):
    off = tmp_path / "off"
    (off / "labels").mkdir(parents=True)
    rows = []
    tr = []
    for c in smoke:
        pk = pk_of(c)
        r = row(c["case_id"], policy.decide(pk.precheck, None, policy.DEFAULT_THR), c["group"], precheck=pk.precheck, cat=c["category"], variant=c["variant"])
        rows.append(r)
        tr.append({"case_id": c["case_id"], "closure_correct": c["author_intent"]["closure_correct"]})
    (off / "replay-smoke.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (off / "labels/truth.jsonl").write_text("".join(json.dumps(t) + "\n" for t in tr))
    out = tmp_path / "out"; out.mkdir()
    v, rule, m, rc = AN.run("smoke", offline=off, out_dir=out, update_matrix=False, tokens={})
    assert v == "GO" and (out / "results.json").exists() and (out / "offline-results.md").read_text().startswith("# E1 offline results: smoke")


# ---------------------------------------------------------------- D6
def test_no_cost_kill():
    pat = re.compile(r"if[^\n]*(spent|running_total|total_tokens|usd|cost)[^\n]*[<>]")
    for f in sorted(E1.glob("*.py")):
        txt = f.read_text()
        assert not pat.search(txt), f.name
    rp = (E1 / "replay.py").read_text()
    assert "break" not in rp.split("for c, pk, st, drift in prepared:")[-1].split("if live:")[0]       # the replay loop never exits early
    dec = A.load_decision(E1 / "decision.toml")
    assert "smoke_false_closure_stop" in dec["rules"] and dec["thresholds"]["freeze_sha"] == ""


def test_freeze_sha_required_before_heldout(tmp_path, smoke):
    dec = A.load_decision(E1 / "decision.toml")
    with pytest.raises(RP.FreezeMissing):
        RP.thresholds_for("heldout", dec, freeze_path=tmp_path / "none.json")
    frz = tmp_path / "freeze.json"
    frz.write_text(json.dumps({"thresholds": {"t_present_low": 0.1, "t_obl_high": 0.9, "t_contra_low": 0.1, "t_ctx_high": 0.9}}))
    d2 = copy.deepcopy(dec); d2["thresholds"]["freeze_sha"] = "0" * 64
    with pytest.raises(RP.FreezeMissing):
        RP.thresholds_for("heldout", d2, frz)
    import hashlib
    d2["thresholds"]["freeze_sha"] = hashlib.sha256(frz.read_bytes()).hexdigest()
    thr, sha = RP.thresholds_for("heldout", d2, frz)
    assert thr["t_obl_high"] == 0.9 and sha == d2["thresholds"]["freeze_sha"]
    assert RP.thresholds_for("smoke", dec)[0] == policy.DEFAULT_THR
