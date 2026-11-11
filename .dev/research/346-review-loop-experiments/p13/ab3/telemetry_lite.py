"""PN3 harness: C8 reviewer_run telemetry records (append-only JSONL). Not product code."""
import datetime
import json
import pathlib
import re
import uuid

import ledger_lite as L

HERE = pathlib.Path(__file__).parent
TEL_DIR = HERE / "telemetry"

TOP = ["schema_version", "kind", "record_id", "ts_utc", "run_id", "step", "round", "reviewer_id", "panel", "slot", "model",
       "task", "output", "cost", "context"]
SUB = {
    "panel": ["template_id", "template_version", "template_sha256", "tiers_version", "tiers_sha256", "environment", "panel_size"],
    "slot": ["slot_id", "tier", "alias", "strategy", "seed", "fallback_depth", "stand_in"],
    "model": ["resolved", "launch", "observed"],
    "task": ["doc_sha256", "doc_bytes", "doc_lines", "language", "doc_format", "specialization", "sections", "max_heading_depth",
             "tables", "table_rows", "ids_defined", "cross_refs", "rfc2119", "review_kind"],
    "output": ["block_ok", "findings", "blocking", "by_severity", "verdict", "verdict_mismatch"],
    "cost": ["tokens_in", "tokens_cache_read", "tokens_cache_write", "tokens_out", "wall_s"],
}
ID_RE = re.compile(r"\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b")


def task_variables(text, specialization="unspecified", review_kind="first"):
    lines = text.split("\n")
    heads = [l for l in lines if re.match(r"^#{1,6}\s", l)]
    tables, rows, i = 0, 0, 0
    while i < len(lines):
        if lines[i].startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            blk = lines[i:j]
            sep = [l for l in blk if re.match(r"^\|\s*:?-{3,}", l)]
            if sep:
                tables += 1
                rows += len(blk) - len(sep) - 1
            i = j
        else:
            i += 1
    defined = set()
    for l in lines:
        m = re.match(r"^\|\s*([^|]+?)\s*\|", l)
        if m:
            defined.update(ID_RE.findall(m.group(1)))
        m2 = re.match(r"^\*\*([^*]+)", l)
        if m2:
            defined.update(ID_RE.findall(m2.group(1)))
    all_ids = ID_RE.findall(text)
    sec_refs = re.findall(r"(?i)\bsection\s+\d+(?:\.\d+)*", text)
    words = re.findall(r"[A-Za-z']+", text.lower())
    common = {"the", "and", "of", "to", "is", "a", "in", "that", "for"}
    lang = "en" if words and sum(w in common for w in words) / len(words) >= 0.02 else "unknown"
    return {"doc_sha256": L.sha(text), "doc_bytes": len(text.encode()), "doc_lines": text.count("\n"), "language": lang,
            "doc_format": "markdown", "specialization": specialization, "sections": len(heads),
            "max_heading_depth": max((len(re.match(r"^#+", h).group(0)) for h in heads), default=0),
            "tables": tables, "table_rows": rows, "ids_defined": len(defined),
            "cross_refs": max(len(all_ids) + len(sec_refs) - len([i for i in all_ids if i in defined]) , 0),
            "rfc2119": len(re.findall(r"\b(?:MUST NOT|MUST|SHALL|SHOULD|MAY|REQUIRED)\b", text)), "review_kind": review_kind}


def reviewer_record(run_id, step, round_n, reviewer, resolution, doc_text, report_text, usage, observed_model, replicate,
                    stratum, review_kind="first", ts=None):
    """reviewer: one entry of a panel resolution; usage: dict(tokens_in, cache_read, cache_write, out, wall_s)."""
    pb = L.parse_block(report_text)
    sev = {"CRITICAL": 0, "MAJOR": 0, "MINOR": 0}
    for f in pb["findings"]:
        sev[f["severity"]] += 1
    blocking = sum(1 for f in pb["findings"] if f["blocking"])
    v = re.findall(r"verdict:\s*\**\s*(PASS|FAIL)", report_text, re.I)
    verdict = v[-1].upper() if v else None
    return {
        "schema_version": "review-telemetry/1", "kind": "reviewer_run", "record_id": uuid.uuid4().hex,
        "ts_utc": ts or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "run_id": run_id, "step": step, "round": round_n, "reviewer_id": reviewer["reviewer_id"],
        "panel": {"template_id": resolution["template_id"], "template_version": resolution["template_version"],
                  "template_sha256": resolution["template_sha256"], "tiers_version": resolution["tiers_version"],
                  "tiers_sha256": resolution["tiers_sha256"], "environment": resolution["environment"],
                  "panel_size": len(resolution["reviewers"])},
        "slot": {"slot_id": reviewer["slot_id"], "tier": reviewer["tier"], "alias": reviewer["alias"], "strategy": reviewer["strategy"],
                 "seed": reviewer["seed"], "fallback_depth": reviewer["fallback_depth"], "stand_in": reviewer["stand_in"]},
        "model": {"resolved": reviewer["model"], "launch": reviewer["launch"], "observed": observed_model},
        "task": task_variables(doc_text, "software-spec", review_kind),
        "output": {"block_ok": pb["ok"], "findings": len(pb["findings"]), "blocking": blocking, "by_severity": sev,
                   "verdict": verdict, "verdict_mismatch": (verdict == "PASS" and blocking > 0) or (verdict == "FAIL" and blocking == 0)},
        "cost": {"tokens_in": usage.get("tokens_in"), "tokens_cache_read": usage.get("cache_read"),
                 "tokens_cache_write": usage.get("cache_write"), "tokens_out": usage.get("out"), "wall_s": usage.get("wall_s")},
        "context": {"experiment": "pn3", "arm": "c3", "replicate": replicate, "stratum": stratum},
    }


def validate(rec):
    errs = []
    if list(rec) != TOP and sorted(rec) != sorted(TOP):
        errs.append(f"top-level keys {sorted(set(rec) ^ set(TOP))}")
    if rec.get("schema_version") != "review-telemetry/1" or rec.get("kind") != "reviewer_run":
        errs.append("schema_version/kind")
    for k, keys in SUB.items():
        if not isinstance(rec.get(k), dict) or sorted(rec[k]) != sorted(keys):
            errs.append(f"{k} keys")
    if not re.match(r"^[A-Za-z0-9._-]{1,64}$", str(rec.get("run_id", ""))):
        errs.append("run_id")
    if not re.match(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$", str(rec.get("ts_utc", ""))):
        errs.append("ts_utc")
    if rec.get("context", {}).get("stratum") not in ("sonnet", "haiku"):
        errs.append("context.stratum")
    return errs


def no_document_text(rec, doc_text, n=40):
    """True if no 40-character substring of the document appears in the serialized record."""
    s = json.dumps(rec)
    flat = " ".join(doc_text.split())
    return not any(flat[i:i + n] in s for i in range(0, max(len(flat) - n, 0), 7))


def write(rec, root=None):
    root = pathlib.Path(root or TEL_DIR)
    ts = rec["ts_utc"]
    d = root / "records" / ts[:4] / ts[5:7]
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{rec['run_id']}.jsonl"
    with open(p, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    return p
