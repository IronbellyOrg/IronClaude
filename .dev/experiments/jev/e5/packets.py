"""E5 session 1: enumerate provisional-PASS packets from frozen run directories (read-only).

A packet is one run whose final review verdict is PASS (the delivered spec was provisionally passed).
Runs whose last review is not PASS are escalated (no provisional PASS) and are listed separately.
Pure helpers take explicit paths so tests can run on fixture trees.
"""
import importlib.util
import json
import os
import pathlib
import re
import sys

sys.dont_write_bytecode = True

SP = pathlib.Path(os.environ.get("SP", "/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad"))
CENTRAL = SP / "central"
AUD_OUT = ".dev/orca-command-refactor/review/audit.md"
REVIEW_DIR = ".dev/orca-command-refactor/review"
FROZEN_SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
REVIEW_CAP = 3

_ST = None


def load_score_themes():
    """Load score_themes from the central byte copy when present, else from p12/ab2 (read-only, no bytecode)."""
    global _ST
    if _ST is not None:
        return _ST
    for cand in (CENTRAL / "score_themes.py", SP / "p12/ab2/score_themes.py"):
        if cand.exists():
            spec = importlib.util.spec_from_file_location("score_themes_e5", cand)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _ST = mod
            return mod
    raise FileNotFoundError("score_themes.py not found")


def default_sources():
    return [
        {"name": "p11", "runs_root": SP / "p11/runs", "stratum": "p11", "design_of": lambda r: "stage2-" + r.split("-")[0],
         "extra_audit_root": SP / "p12/baseline-audit2", "require_both_audits": False},
        {"name": "p14", "runs_root": SP / "p14/haiku-baseline/runs", "stratum": "p14", "design_of": lambda r: "p14-haiku-a3",
         "extra_audit_root": None, "require_both_audits": False},
        {"name": "p12-ab1", "runs_root": SP / "p12/ab1/runs", "stratum": "other", "design_of": lambda r: "p12-ab1",
         "extra_audit_root": None, "require_both_audits": True},
        {"name": "p12-ab2", "runs_root": SP / "p12/ab2/runs", "stratum": "other", "design_of": lambda r: "p12-ab2",
         "extra_audit_root": None, "require_both_audits": True},
        {"name": "p12-ab3", "runs_root": SP / "p12/ab3/runs", "stratum": "other", "design_of": lambda r: "p12-ab3",
         "extra_audit_root": None, "require_both_audits": True},
        {"name": "p13-ab1", "runs_root": SP / "p13/ab1/runs", "stratum": "other", "design_of": lambda r: "p13-pn1",
         "extra_audit_root": None, "require_both_audits": True},
        {"name": "p13-ab2", "runs_root": SP / "p13/ab2/runs", "stratum": "other", "design_of": lambda r: "p13-pn2",
         "extra_audit_root": None, "require_both_audits": True},
    ]


def audit_paths(run_dir, run_name, extra_audit_root=None):
    """Existing frozen audit files for a run: aud, aud2 and (baseline) the second-audit tree."""
    run_dir = pathlib.Path(run_dir)
    out = []
    for sub in ("aud", "aud2"):
        p = run_dir / sub / "ws" / AUD_OUT
        if p.exists():
            out.append(p)
    if extra_audit_root is not None:
        p = pathlib.Path(extra_audit_root) / run_name / "ws" / AUD_OUT
        if p.exists():
            out.append(p)
    return out


def _step_order(state):
    log = state.get("log", {})
    order = [s for s in state.get("done", []) if s in log]
    for s in log:
        if s not in order:
            order.append(s)
    return order


def review_sequence(state):
    """Ordered whole/scoped review steps: R<k> (or merged M<k> in panel designs), G and GR (gate reviews)."""
    log = state.get("log", {})
    order = _step_order(state)
    has_merge = any(re.fullmatch(r"M\d+", s) for s in order)
    out = []
    for s in order:
        if (re.fullmatch(r"R\d+", s) and not has_merge) or re.fullmatch(r"M\d+", s) or s in ("G", "GR"):
            out.append(s)
    return out


def _report_path(run_dir, step):
    base = pathlib.Path(run_dir) / "ws" / REVIEW_DIR
    m = re.fullmatch(r"[RM](\d+)", step)
    cand = []
    if m:
        cand.append(base / f"round{m.group(1)}.md")
    elif step == "G":
        cand.append(base / "gate.md")
    elif step == "GR":
        cand.append(base / "gate-round2.md")
    for c in cand:
        if c.exists():
            return c
    return cand[0] if cand else None


def count_followups(report_path):
    """Bullets under the 'Follow-up candidates' heading (0 when absent)."""
    try:
        t = pathlib.Path(report_path).read_text(errors="ignore")
    except OSError:
        return 0
    m = re.search(r"(?ims)^#+\s*Follow-up candidates[^\n]*\n(.*?)(?=^#+ |^verdict:|\Z)", t)
    if not m:
        return 0
    return len(re.findall(r"(?m)^\s*[-*]\s+\S", m.group(1)))


def parsed_ids_in_report(report_path):
    """Ids that score_themes.ids_from/parse_ids extract from a report (prose ids on a PASS are artifacts)."""
    st = load_score_themes()
    try:
        return len(st.parse_ids(st.ids_from(report_path)))
    except OSError:
        return 0


def count_open_blockers(report_path):
    """Open blockers after a review: 0 when the report's verdict is PASS (a PASS means no blocking finding is open;
    ids a PASS report names are resolved or restated, see parsed_ids_in_report), else the parsed blocking ids."""
    st = load_score_themes()
    try:
        text = pathlib.Path(report_path).read_text(errors="ignore")
    except OSError:
        return 0
    if st.verdict_of(text) == "PASS":
        return 0
    return parsed_ids_in_report(report_path)


def build_packet(run_dir, state, *, design, stratum, initial_sha=FROZEN_SPEC_SHA):
    """Return ("packet"|"escalated"|"excluded", dict)."""
    run_dir = pathlib.Path(run_dir)
    log = state.get("log", {})
    order = _step_order(state)
    reviews = review_sequence(state)
    if not reviews:
        return "excluded", {"run": state.get("run", run_dir.name), "reason": "no review steps"}
    # running spec hash, hash reviewed by each review, fix cycles, whole-review hashes
    cur = initial_sha
    sha_at = {}
    fix_cycles = 0
    fix_at = {}
    for s in order:
        sa = (log[s].get("spec_after") or {}).get("sha256") if isinstance(log[s], dict) else None
        if sa:
            cur = sa
        if s in reviews:
            sha_at[s] = cur
            fix_at[s] = fix_cycles
        if re.fullmatch(r"V\d+", s):
            fix_cycles += 1
    delivered = (state.get("final_spec") or {}).get("sha256") or cur
    last = reviews[-1]
    verdict = log[last].get("verdict")
    run = state.get("run", run_dir.name)
    if verdict != "PASS":
        return "escalated", {"run": run, "design": design, "stratum": stratum, "reviews": len(reviews),
                             "last_review": last, "last_verdict": verdict}
    k = len(reviews)
    whole_shas = set()
    for i, s in enumerate(reviews):
        if i == 0 or s == "G":
            whole_shas.add(sha_at[s])
    # PASS review is whole itself when first or a gate, which then covers its own hash; a scoped PASS does not
    changed = sha_at[last] not in whole_shas
    report = _report_path(run_dir, last)
    return "packet", {
        "run": run, "design": design, "stratum": stratum, "review_k": k, "slots_remaining": max(0, REVIEW_CAP - k),
        "fix_cycles_used": fix_at[last], "spec_sha_at_pass": sha_at[last],
        "changed_since_last_whole_review": changed,
        "open_blockers": count_open_blockers(report) if report and report.exists() else 0,
        "parsed_ids_in_pass_report": parsed_ids_in_report(report) if report and report.exists() else 0,
        "followups": count_followups(report) if report else 0,
        "verdict_source": str(report) if report else None,
        "pass_step": last, "delivered_matches_pass": sha_at[last] == delivered,
        "mandatory_policy": False,
    }


def enumerate_packets(sources):
    packets, escalated, excluded = [], [], []
    for src in sources:
        root = pathlib.Path(src["runs_root"])
        if not root.is_dir():
            continue
        for run_dir in sorted(p for p in root.iterdir() if p.is_dir() and (p / "state.json").exists()):
            try:
                state = json.loads((run_dir / "state.json").read_text())
            except (OSError, ValueError) as e:
                excluded.append({"run": run_dir.name, "source": src["name"], "reason": f"state.json unreadable: {e}"})
                continue
            run = state.get("run", run_dir.name)
            auds = audit_paths(run_dir, run_dir.name, src.get("extra_audit_root"))
            need = 2 if src.get("require_both_audits") else 1
            if len(auds) < need:
                excluded.append({"run": run, "source": src["name"], "reason": f"audits available {len(auds)} < {need}"})
                continue
            kind, rec = build_packet(run_dir, state, design=src["design_of"](run_dir.name), stratum=src["stratum"])
            rec["source"] = src["name"]
            rec["audit_paths"] = [str(a) for a in auds]
            {"packet": packets, "escalated": escalated, "excluded": excluded}[kind].append(rec)
    return {"packets": packets, "escalated": escalated, "excluded": excluded}


def main():
    import datetime
    res = enumerate_packets(default_sources())
    res["generated_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    out = pathlib.Path(__file__).parent / "offline" / "packets.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(res, indent=1))
    print(f"packets={len(res['packets'])} escalated={len(res['escalated'])} excluded={len(res['excluded'])} -> {out}")


if __name__ == "__main__":
    main()
