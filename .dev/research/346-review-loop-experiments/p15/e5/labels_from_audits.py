"""E5 session 1: independent labels from the frozen audits (no Jev, no author, no worker)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import packets as pk  # noqa: E402


def audit_summary(path):
    st = pk.load_score_themes()
    p = pathlib.Path(path)
    text = p.read_text(errors="ignore")
    verdict = st.verdict_of(text)
    blocking = len(st.blocking_findings(p)) if verdict == "FAIL" else 0
    return {"path": str(p), "verdict": verdict, "blocking": blocking}


def label_audits(audits):
    """audits: list of {"verdict", "blocking"}.

    Strict (primary): needs_assurance = yes when ANY usable audit has a blocking finding, else no.
    Sensitivity: adequate (no) when at least one usable audit PASSes, else yes.
    Usable = verdict PASS or FAIL; no usable audit -> unlabeled.
    """
    usable = [a for a in audits if a["verdict"] in ("PASS", "FAIL")]
    if not usable:
        return {"label": "unlabeled", "sens_label": "unlabeled", "n_audits": len(audits), "single_audit": len(audits) < 2,
                "fail_unparsed": 0}
    strict = "yes" if any(a["blocking"] > 0 for a in usable) else "no"
    sens = "no" if any(a["verdict"] == "PASS" for a in usable) else "yes"
    return {"label": strict, "sens_label": sens, "n_audits": len(usable), "single_audit": len(usable) < 2,
            "fail_unparsed": sum(1 for a in usable if a["verdict"] == "FAIL" and a["blocking"] == 0)}


def label_packet(packet):
    audits = [audit_summary(p) for p in packet["audit_paths"]]
    out = label_audits(audits)
    out["audits"] = [{"verdict": a["verdict"], "blocking": a["blocking"], "path": a["path"]} for a in audits]
    return out
