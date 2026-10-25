"""Replay oracle for /sc:implement severity and convergence (SPEC AC-08, AC-09).

Scope: this oracle checks that the rules are internally consistent. It is a
short pure-function reference written from the same spec as the protocol text
(FR-001..FR-004, the parent-computed verdict, FR-011 origin caps, FR-014
convergence, probe before locality, FR-024/FR-017 locality and repair caps, the
notes chain rule), fed transcribed finding lines from SPEC Section 10. It does
NOT test the protocol text; that coverage comes from
tests/skills/test_implement_severity_static.py.

AC-13 (model-free protocol walkthrough) cannot be driven here: the protocol is
model-executed prose. Its manual check lives in the plan package at
artifacts/t11-ac13-manual-check.md.
"""

TRIGGERS = ("B1", "B2", "B3", "B4")  # amiss, false, harm, constraint


def fnd(
    id,
    chk="nnnn",
    origin="new",
    ac="T1.AC1",
    family=None,
    file="README.md",
    readback=True,
    cosmetic=False,
    text=None,
):
    return dict(
        id=id,
        chk=chk,
        origin=origin,
        ac=ac,
        family=family or id,
        file=file,
        readback=readback,
        cosmetic=cosmetic,
        text=text or id,
    )


# --- FR-001..FR-004 + FR-011: parent-derived severity ---------------------------
def severity(f):
    confirmed = "y" in f["chk"] and f["readback"]
    if confirmed:
        return "note" if f["origin"] == "inherited" else "blocking"
    if (
        "y" in f["chk"] or f["cosmetic"] or f["origin"] in ("inherited", "late")
    ):  # failed Read-back
        return "note"
    return "minor"


def trigger(f):
    return TRIGGERS[f["chk"].index("y")] if severity(f) == "blocking" else "none"


def blockers(findings):
    return [f for f in findings if severity(f) == "blocking"]


# --- Verdict owner correction: parent runs the closed order over blockers only ---
def verdict(marks, findings, acs, diff_empty=False):
    """marks: {ac: (state, citation, [finding ids])}. Returns verdict or paperwork."""
    for state, cite, ids in marks.values():
        if not cite or (state == "unmet" and not ids):
            return "reviewer-paperwork"  # FR-031: respawn once, then reviewer-down
    blk = blockers(findings)
    unmet = {
        a
        for f in blk
        if trigger(f) in ("B1", "B2")
        for a in (acs if f["ac"] == "scope" else [f["ac"]])
    }
    if diff_empty:
        return "cannot-verify"
    if unmet:
        return "missing"
    if any(trigger(f) in ("B3", "B4") for f in blk):
        return "extra"
    return "compliant"


def met_marks(acs):
    return {a: ("met", f"{a}@README.md:1", []) for a in acs}


# --- FR-014 convergence ------------------------------------------------------
def count(findings, all_severity=False):
    return (
        len(findings)
        if all_severity
        else len({f["family"] for f in blockers(findings)})
    )


def fix_failed(targeted, next_review):
    open_fams = {f["family"] for f in blockers(next_review)}
    return bool(open_fams & targeted) or any(
        f["origin"] == "fix-induced" for f in blockers(next_review)
    )


# --- Probe before locality + FR-024 locality + FR-017 repair caps -------------
def probe_only(families, probes):
    """Write a probe-only entry (no after: lines) for every probe-pending family."""
    for fam in families - probes.keys():
        probes[fam] = dict(
            form=fam, cmd=f"grep -nE {fam!r} README.md", before="hit", coupled=[]
        )
    return probes


def complete(entry):
    return all(entry.get(k) is not None for k in ("form", "cmd", "before", "coupled"))


def local(findings, probes):
    blk = blockers(findings)
    fams = {f["family"] for f in blk}
    return (
        len(fams) <= 5
        and len({f["file"] for f in blk}) <= 2
        and not any(f["chk"][0] == "y" for f in blk)
        and all(complete(probes.get(fam, {})) for fam in fams)
    )


def route(k, findings, probes, repairs, prior_failed=False, first_repair_ok=True):
    """Outcome after a review of attempt k: complete / repair / adviser."""
    blk = blockers(findings)
    if not blk:
        return "complete"
    probe_only({f["family"] for f in blk}, probes)
    second_a2 = (
        k == 2
        and repairs == 1
        and first_repair_ok
        and all(f["origin"] == "late" for f in blk)
    )
    cap_ok = repairs < 2 and (repairs == 0 or second_a2)
    return (
        "repair"
        if not prior_failed and k >= 2 and cap_ok and local(findings, probes)
        else "adviser"
    )


def inline_may_complete(findings, notes_lines):
    return not findings and len(notes_lines) <= 1


# --- Notes chain rule ----------------------------------------------------------
def notes_rewrite(start, appended, final_tree):
    """appended: [(review id, finding)] from failing reviews of the current chain."""
    keep = [f"{r} {f['id']}" for r, f in appended if f["text"] in final_tree]
    gone = [
        f"superseded {r} {f['id']}" for r, f in appended if f["text"] not in final_tree
    ]
    return [start] + keep + gone, 1 + len(keep)


# --- FR-010 origin ---------------------------------------------------------------
def origin(text, start, chain):
    """chain: [(tree texts, flagged texts, written_by_fix)] oldest first; last = current."""
    if text in start:
        return "inherited"
    if any(text in t and text not in fl for t, fl, _ in chain[:-1]):
        return "late"
    first = next(c for c in chain if text in c[0])
    return "fix-induced" if first[2] else "new"


# ================================ cases =========================================
ACS = ["T1.AC1", "T1.AC2", "T1.AC3", "T1.AC4"]

R_A1 = [
    fnd("D1", "nynn", family="guard"),
    fnd("D2", "nynn", family="restore"),
    fnd("readme", "nnny", readback=False),
    fnd("D3", cosmetic=True, text="a1-pipe"),
    fnd("D4", text="a1-broad"),
]
R_A2 = [fnd("write", "nnyn", origin="late", family="data-write")]
R_A3 = [
    fnd("D1", "nynn", origin="late", family="sample"),
    fnd("D2", "nynn", origin="late", family="jq"),
    fnd("D3", "nnny", readback=False),
    fnd("D4", origin="late"),
]
R_A4 = [fnd("serena", origin="fix-induced"), fnd("row2"), fnd("wording", cosmetic=True)]
R_A5 = [
    fnd("tar", "nnyn", origin="inherited"),
    fnd("chmod", "nnyn", origin="inherited"),
    fnd("rows"),
    fnd("snippet", origin="fix-induced"),
]


def sevs(fs):
    return [severity(f) for f in fs]


def test_r_a1_blocks_with_readback_dependent_constraint():
    assert sevs(R_A1) == ["blocking", "blocking", "note", "note", "minor"]
    assert verdict(met_marks(ACS), R_A1, ACS) == "missing"


def test_r_a2_low_label_ignored_blocks_and_probe_before_locality_repairs():
    assert sevs(R_A2) == ["blocking"] and trigger(R_A2[0]) == "B3"
    probes = {}  # data-write family first raised at A2: no probe yet
    assert not local(R_A2, probes)  # would be non-local without the probe-only step
    assert route(2, R_A2, probes, repairs=0) == "repair"
    assert "after" not in probes["data-write"] and complete(
        probes["data-write"]
    )  # V3 F-05


def test_r_a3_late_blockers_local_second_a2_repair():
    assert sevs(R_A3) == ["blocking", "blocking", "note", "note"]
    assert route(2, R_A3, {}, repairs=1) == "repair"
    assert route(2, R_A3, {}, repairs=1, first_repair_ok=False) == "adviser"
    assert route(2, R_A3, {}, repairs=2) == "adviser"


def test_r_a4_passes_with_notes():
    assert sevs(R_A4) == ["minor", "minor", "note"]
    assert (
        verdict(met_marks(ACS), R_A4, ACS) == "compliant"
        and route(4, R_A4, {}, 0) == "complete"
    )


def test_r_a5_parent_caps_inherited_harm_and_computes_compliant():
    assert all(f["chk"][2] == "y" for f in R_A5[:2])  # reviewer said harmful-effect=yes
    assert sevs(R_A5) == ["note", "note", "minor", "minor"]
    assert verdict(met_marks(ACS), R_A5, ACS) == "compliant"
    assert route(5, R_A5, {}, 0) == "complete"  # notes, no fix pass


def test_t1_end_state_and_notes_chain():
    reviews = [("r1-1", R_A1), ("r2-1", R_A2), ("r2-2", R_A3), ("r2-3", [])]
    probes, repairs, notes, ledger = {}, 0, [], ["T1: start sha=05644ca4"]
    for rid, fs in reviews[1:]:  # A1 failure goes to the Q5 fix pass, not a repair
        notes += [(rid, f) for f in fs if severity(f) != "blocking"]
        r = route(2, fs, probes, repairs)
        if r == "repair":
            repairs += 1
    notes = [("r1-1", f) for f in R_A1 if severity(f) != "blocking"] + notes
    assert r == "complete" and repairs == 2 and len(reviews) == 4
    final_tree = {"readme", "a1-broad", "D3", "D4"}  # the A1 pipe text was fixed away
    lines, m = notes_rewrite("05644ca4", notes, final_tree)
    ledger.append(
        f"T1: complete verdict={verdict(met_marks(ACS), [], ACS)} ac={','.join(ACS)} "
        f"evidence=notes@retries/T1/notes.md:1-{m} files=README.md"
    )
    assert "verdict=compliant" in ledger[1] and len(ledger) == 2
    assert not any("revert" in x or "halt" in x or "Ruling:" in x for x in ledger)
    assert all(not x.startswith("superseded") for x in lines[1:m])
    assert {x.split()[0] for x in lines[1:m]} == {"r1-1", "r2-2"}
    assert all(x.startswith("superseded") for x in lines[m:])


PV_R1 = [
    [fnd(f"I{i}", "nynn", family=f"f{i}") for i in range(6)],
    [fnd(f"I{i}", "nynn", family=f"f{i}") for i in range(5)]
    + [fnd("B2-N2", "nynn", origin="fix-induced", family="n2")]
    + [fnd(f"m{i}") for i in range(6)],
    [fnd(f"I{i}", "nynn", family=f"f{i}") for i in range(3)]
    + [fnd("S-N3r3", "nynn", origin="late", family="s3")]
    + [fnd(f"m{i}") for i in range(10)],
]


def pv_r1(all_severity=False):
    counts = [count(r, all_severity) for r in PV_R1]
    return (
        counts,
        fix_failed({f"f{i}" for i in range(6)}, PV_R1[1]),
        counts[2] < counts[1],
    )


def test_pv_r1_counts_blocking_families_only():
    assert pv_r1() == ([6, 6, 4], True, True)


def test_pv_r1_all_severity_flip_changes_outcome():
    assert pv_r1(all_severity=True) != pv_r1()
    assert pv_r1(all_severity=True)[2] is False  # 14 > 12: progress lost


def test_v3_f01_unmet_behind_non_blocking_completes():
    for f in (fnd("x", "ynnn", readback=False), fnd("y", "nynn", origin="inherited")):
        marks = met_marks(ACS) | {"T1.AC1": ("unmet", "T1.AC1@README.md:3", [f["id"]])}
        assert (
            verdict(marks, [f], ACS) == "compliant"
            and route(2, [f], {}, 0) == "complete"
        )
    assert (
        verdict({"T1.AC1": ("unmet", "T1.AC1@README.md:3", [])}, [], ACS)
        == "reviewer-paperwork"
    )


def test_v3_f03_scope_blocker_never_compliant():
    assert verdict(met_marks(ACS), [fnd("s", "nynn", ac="scope")], ACS) == "missing"
    for fs in (R_A1, R_A2, R_A3, R_A4, R_A5, *PV_R1):
        if blockers(fs):
            assert verdict(met_marks(ACS), fs, ACS) != "compliant"


def test_v3_f02_inline_after_failing_review_reruns_as_subagent():
    notes = ["05644ca4", "r1-1 D4"]  # failing A1 appended minors
    assert not inline_may_complete([], notes)
    assert inline_may_complete([], notes[:1])


def test_ac09_addendum1_origin_fixture():
    start = {"tar"}
    chain = [  # (tree, flagged, written by in-place fix)
        ({"tar", "write", "sample", "recorder"}, set(), False),  # A1
        ({"tar", "write", "sample", "recorder", "jq"}, {"write"}, True),  # A2 fix pass
        ({"tar", "sample", "recorder", "jq"}, {"sample", "jq"}, True),  # repair
        ({"tar", "recorder", "serena"}, {"serena"}, True),  # later fix tree
        ({"tar", "recorder", "serena", "snippet"}, set(), True),  # current fix tree
    ]
    # ponytail: one linear chain stands in for the per-attempt diffs of SB:85-93.
    raised = ["write", "sample", "jq", "recorder", "serena", "tar", "snippet"]
    origins = [
        origin(t, start, chain[:i]) for t, i in zip(raised, (2, 3, 3, 5, 4, 5, 5))
    ]
    assert origins == [
        "late",
        "late",
        "late",
        "late",
        "fix-induced",
        "inherited",
        "fix-induced",
    ]
