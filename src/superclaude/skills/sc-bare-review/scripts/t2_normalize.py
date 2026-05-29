#!/usr/bin/env python3
"""t2_normalize.py — sc-bare-review Wave D (template normalization) + Wave E (return contract).

Reads the manifest emitted by ``t2_preflight.sh``, and for each reviewer reads its
``.raw`` output + ``.meta.json`` sidecar (from ``t2_dispatch.sh``), normalizes the model
output into the compressed-markdown template (``refs/output-template.md``), writes the
final ``.md`` atomically with a deterministic filename (IMM-6), then determines aggregate
status (IMM-5, success-first) and emits the Wave-E return contract — always, including on
failure (write-on-failure pattern).

Usage:  t2_normalize.py --manifest <output>/manifest.json

Spec: merged-requirements.md §3.3 Wave D/E, §4, §7.4, §9.1 (AC-1.8..AC-1.12).
No third-party deps (stdlib only) — the contract/frontmatter YAML is hand-emitted.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone

SEV_ALIASES = {
    "crit": "crit", "critical": "crit", "blocker": "crit",
    "high": "high", "major": "high",
    "med": "med", "medium": "med", "moderate": "med",
    "low": "low", "minor": "low",
    "nit": "nit", "nitpick": "nit", "trivial": "nit", "info": "nit",
}
EMPTY_CITE = {"", "none", "n/a", "na", "-", "--"}
FINDING_ID = re.compile(r"^f-?\d+$", re.IGNORECASE)


def iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def yaml_str(v: str) -> str:
    """Double-quote a scalar for safe single-line YAML emission."""
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def strip_frontmatter(text: str) -> str:
    if text.lstrip().startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def normalize_sev(cell: str) -> str:
    return SEV_ALIASES.get(cell.strip().lower(), "med")


def normalize_cite(cell: str) -> str:
    return "none" if cell.strip().lower() in EMPTY_CITE else cell.strip()


def parse_conf(cell: str) -> str:
    m = re.search(r"\d+", cell)
    if not m:
        return ""
    return str(max(0, min(100, int(m.group()))))


def parse_findings(text: str) -> list[dict]:
    findings: list[dict] = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 5 or not FINDING_ID.match(cells[0]):
            continue
        claim = cells[2].replace("\n", " ").strip()[:120]
        if not claim:
            continue
        findings.append({
            "sev": normalize_sev(cells[1]),
            "claim": claim,
            "cite": normalize_cite(cells[3]),
            "conf": parse_conf(cells[4]),
        })
    return findings


def extract_section(text: str, heading: str, cap: int) -> str:
    m = re.search(rf"^#+\s*{re.escape(heading)}\s*$", text, re.IGNORECASE | re.MULTILINE)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^#+\s", rest, re.MULTILINE)
    body = rest[: nxt.start()] if nxt else rest
    return " ".join(body.split())[:cap]


def render_markdown(slug: str, fm: dict, findings: list[dict], verdict: str, notes: str) -> str:
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, int):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f"{k}: {yaml_str(v)}")
    lines.append("---")
    lines += ["", f"# T2-Bare Review — {slug}", "", "## Findings", ""]
    lines += ["| ID | Sev | Claim | Cite | SelfConf |", "|----|-----|-------|------|----------|"]
    for i, f in enumerate(findings, 1):
        lines.append(f"| F-{i:02d} | {f['sev']} | {f['claim']} | {f['cite']} | {f['conf']} |")
    lines += ["", "## Verdict", verdict or "(no verdict returned)"]
    if notes:
        lines += ["", "## Notes", notes]
    return "\n".join(lines) + "\n"


def atomic_write(path: str, content: str) -> int:
    """IMM-6: write-to-tmp + os.replace; deterministic path makes re-runs idempotent."""
    data = content.encode("utf-8")
    tmp = f"{path}.tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)
    return len(data)


def normalize_reviewer(rv: dict, target: str, checksum: str, truncated: bool, label: str) -> dict:
    """Return an output_files record; writes the final .md on success."""
    rec = {
        "path": rv["final_path"], "model_id": rv["model_id"],
        "model_label": rv["model_label"], "bytes": 0,
        "status": "proxy_error", "elapsed_ms": 0,
    }
    meta = {}
    if os.path.exists(rv["meta_path"]):
        try:
            meta = json.loads(open(rv["meta_path"], encoding="utf-8").read())
        except (json.JSONDecodeError, OSError):
            meta = {}
    rec["status"] = meta.get("status", "proxy_error")
    rec["elapsed_ms"] = int(meta.get("elapsed_ms", 0) or 0)

    raw = ""
    if os.path.exists(rv["raw_path"]):
        try:
            raw = open(rv["raw_path"], encoding="utf-8", errors="replace").read()
        except OSError:
            raw = ""

    # Hard failures never produce a file; keep .raw for triage (§8).
    if rec["status"] in ("timeout", "proxy_error") or not raw.strip():
        if rec["status"] == "success":
            rec["status"] = "proxy_error"
        return rec

    body = strip_frontmatter(raw)
    findings = parse_findings(body)
    verdict = extract_section(body, "Verdict", 300)
    notes = extract_section(body, "Notes", 200)

    # §7.4 salvage: a parse_error reviewer with a recoverable body is promoted to success.
    if rec["status"] == "parse_error":
        if not findings and not verdict:
            return rec  # genuinely unparseable — stays failed, .raw retained
    elif not findings and not verdict:
        verdict = " ".join(body.split())[:300] or "(no structured findings returned)"

    slug = os.path.splitext(os.path.basename(target))[0]
    fm = {
        "schema_version": "1.0", "tier": "T2", "suspect": True,
        "reviewer_model_id": rv["model_id"], "reviewer_model_label": rv["model_label"],
        "target": target, "target_checksum": checksum, "target_truncated": truncated,
        "generated": iso_now(), "caller_label": label,
        "elapsed_ms": rec["elapsed_ms"], "finding_count": len(findings),
    }
    rec["bytes"] = atomic_write(rv["final_path"], render_markdown(slug, fm, findings, verdict, notes))
    rec["status"] = "success"
    try:
        os.remove(rv["raw_path"])  # Wave D.3: drop .raw on success
    except OSError:
        pass
    return rec


def emit_contract(path: str, fields: dict, output_files: list[dict]) -> str:
    lines = [
        'contract_version: "1.0"',
        f"status: {fields['status']}",
        f"target: {yaml_str(fields['target'])}",
        f"target_checksum: {yaml_str(fields['checksum'])}",
        f"target_truncated: {'true' if fields['truncated'] else 'false'}",
        f"reviewers_requested: {fields['requested']}",
        f"reviewers_succeeded: {fields['succeeded']}",
        "output_files:",
    ]
    if not output_files:
        lines[-1] = "output_files: []"
    for f in output_files:
        lines += [
            f"  - path: {yaml_str(f['path'])}",
            f"    model_id: {yaml_str(f['model_id'])}",
            f"    model_label: {yaml_str(f['model_label'])}",
            f"    bytes: {f['bytes']}",
            f"    status: {f['status']}",
            f"    elapsed_ms: {f['elapsed_ms']}",
        ]
    lines.append("suspect: true")
    lines.append(f"recommended_next_command: {yaml_str(fields['next_cmd'])}")
    text = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description="sc-bare-review Wave D/E normalizer")
    ap.add_argument("--manifest", required=True)
    args = ap.parse_args()

    with open(args.manifest, encoding="utf-8") as fh:
        man = json.load(fh)

    target = man["target"]
    checksum = man["target_checksum"]
    truncated = bool(man["target_truncated"])
    label = man.get("caller_label", "") or ""
    requested = int(man["reviewers_requested"])

    output_files = [
        normalize_reviewer(rv, target, checksum, truncated, label)
        for rv in man["reviewers"]
    ]
    succeeded = [f for f in output_files if f["status"] == "success"]
    m = len(succeeded)

    # IMM-5 (success-first): M==N → success; 2<=M<N → partial; M<2 → failed.
    if m == requested:
        status = "success"
    elif m >= 2:
        status = "partial"
    else:
        status = "failed"

    success_paths = [f["path"] for f in succeeded]
    compare = ",".join(["<existing-review>", *success_paths])
    suspect = ",".join(success_paths) if success_paths else "<no-bare-files>"
    next_cmd = f"/sc:adversarial --compare {compare} --suspect-source {suspect}"

    contract_text = emit_contract(
        man["contract_path"],
        {"status": status, "target": target, "checksum": checksum,
         "truncated": truncated, "requested": requested, "succeeded": m,
         "next_cmd": next_cmd},
        output_files,
    )
    print(contract_text, end="")
    # Exit 0 always: status lives in the contract; M<2 is a domain outcome, not a crash.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
