"""Typed finding ledger (review-ledger/1): rows, statuses and the verdict.

Only this module changes a finding's status; a reviewer's own prior lines are
recorded as notes and never change one. Deterministic, standard library only.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from typing import Any, Sequence

from superclaude.cli.review import findings as fnd

SCHEMA = "review-ledger/1"
CAPTURE_SCHEMA = "review-capture/1"
STATUSES = ("open", "resolved_check", "resolved", "regressed", "deferred")
_SEV_RANK = {"MINOR": 0, "MAJOR": 1, "CRITICAL": 2}

REVISER_RULES = (
    "Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; "
    "add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; "
    "prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id."
)


class LedgerError(Exception):
    """A ledger operation was refused (wrong round, unknown row, unreadable file)."""


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def new_ledger(doc: str, cap: int = 3) -> dict:
    return {"schema": SCHEMA, "doc": doc, "cap_reviews": cap, "rounds": [], "rows": []}


def load(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            obj = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise LedgerError(f"cannot read ledger {path}: {exc}") from exc
    if not isinstance(obj, dict) or obj.get("schema") != SCHEMA:
        raise LedgerError(f"{path} is not a {SCHEMA} file")
    return obj


def save(ledger: dict, path: str) -> None:
    """Write the ledger atomically (temp file in the same directory, then os.replace)."""
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".ledger-", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(ledger, fh, indent=1, ensure_ascii=False)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def _row(ledger: dict, lid: str) -> dict:
    for r in ledger["rows"]:
        if r["lid"] == lid:
            return r
    raise LedgerError(f"unknown ledger id {lid}")


def _view(row: dict) -> dict:
    return {
        "fp": row["fp"],
        "span": row.get("span"),
        "span2": row.get("span2"),
        "refs_norm": row.get("refs", []),
    }


def _confidence(row: dict) -> str:
    per_round: dict[int, set[str]] = {}
    for m in row["members"]:
        per_round.setdefault(m["round"], set()).add(m["reviewer_id"])
    return "overlap" if any(len(v) >= 2 for v in per_round.values()) else "single"


def _decision(ledger: dict, verdict: str, n: int) -> str:
    if verdict == "PASS":
        return "PASS"
    return "REVISE" if n < ledger["cap_reviews"] else "ESCALATE"


def _brief_ids(ledger: dict) -> list[str]:
    return [
        r["lid"]
        for r in ledger["rows"]
        if r["blocking"] and r["status"] in ("open", "regressed")
    ]


def merge_round(ledger: dict, doc_text: str, n: int, reviewers: Sequence[dict]) -> dict:
    """Merge the reports of round n into the ledger and compute the verdict and decision.

    reviewers: dicts with reviewer_id, model, report_path and text, in resolution order.
    Raises LedgerError, changing nothing, when no reviewer produced a valid findings block.
    A reviewer with an invalid block is skipped for clearing but its parsable findings are kept.
    """
    expected = len(ledger["rounds"]) + 1
    if n != expected:
        raise LedgerError(
            f"round {n} cannot be merged: the ledger expects round {expected}"
        )
    ids = [r["reviewer_id"] for r in reviewers]
    if len(set(ids)) != len(ids):
        raise LedgerError("duplicate reviewer id in one round")
    warnings: list[str] = []
    block_ok: dict[str, bool] = {}
    entries: list[dict] = []
    all_findings: list[dict] = []
    priors: list[tuple[str, dict]] = []
    for rv in reviewers:
        parsed = fnd.parse_block(rv["text"])
        block_ok[rv["reviewer_id"]] = parsed["ok"]
        if not parsed["ok"]:
            msg = parsed["errors"][0]["msg"] if parsed["errors"] else "unknown error"
            warnings.append(
                f"{rv['reviewer_id']}: findings block problem ({len(parsed['errors'])} error(s)), first: {msg}"
            )
        for f in parsed["findings"]:
            a = fnd.annotate(f, doc_text)
            a["_reviewer"] = rv["reviewer_id"]
            all_findings.append(a)
        for p in parsed["priors"]:
            priors.append((rv["reviewer_id"], p))
        entries.append(
            {
                "reviewer_id": rv["reviewer_id"],
                "model": rv.get("model"),
                "report": rv.get("report_path"),
                "report_sha256": sha256_text(rv["text"]),
                "block_ok": parsed["ok"],
            }
        )
    if not any(block_ok.values()):
        # No reviewer produced a valid findings block (a report that is incomplete, lacks the block, has a
        # malformed or unclosed block). That is not a clean review: refuse the merge before anything is
        # recorded so the round can be re-run, never certify PASS on a review that did not happen.
        raise LedgerError(
            f"round {n} cannot be merged: no reviewer produced a valid findings block "
            f"({'; '.join(w for w in warnings)}). Re-run the review; the ledger was not changed."
        )
    existing = list(ledger["rows"])
    new_lids: list[str] = []
    refound: list[str] = []
    regressed: list[str] = []
    cleared: list[str] = []
    cluster_info: list[dict] = []
    members_by_lid: dict[str, list[dict]] = {}
    for group in fnd.cluster(all_findings):
        match = None
        for row in existing:
            view = _view(row)
            if any(fnd.same_defect(m, view) for m in group):
                match = row
                break
        member_recs = [
            {
                "round": n,
                "reviewer_id": m["_reviewer"],
                "fid": m["id"],
                "blocking": bool(m["blocking"]),
            }
            for m in group
        ]
        if match is None:
            first = group[0]
            refs = sorted({t for m in group for t in m["refs_norm"]})
            row = {
                "lid": f"L{len(ledger['rows']) + 1}",
                "fp": first["fp"],
                "blocking": any(m["blocking"] for m in group),
                "severity_max": max(
                    (m["severity"] for m in group), key=lambda s: _SEV_RANK[s]
                ),
                "category": first["category"],
                "confidence": "single",
                "status": "open",
                "anchor": first["anchor"],
                "anchor2": first.get("anchor2"),
                "span": list(first["span"]) if first["span"] else None,
                "span2": list(first["span2"]) if first["span2"] else None,
                "refs": refs,
                "claim": first["claim"],
                "members": member_recs,
                "history": [{"round": n, "event": "opened"}],
            }
            row["confidence"] = _confidence(row)
            ledger["rows"].append(row)
            new_lids.append(row["lid"])
            event = "opened"
        else:
            row = match
            row["members"].extend(member_recs)
            row["blocking"] = any(m["blocking"] for m in row["members"])
            row["severity_max"] = max(
                [row["severity_max"], *[m["severity"] for m in group]],
                key=lambda s: _SEV_RANK[s],
            )
            row["confidence"] = _confidence(row)
            row["history"].append({"round": n, "event": "refound"})
            refound.append(row["lid"])
            event = "refound"
            if row["status"] in ("resolved_check", "resolved"):
                row["status"] = "regressed"
                regressed.append(row["lid"])
                event = "regressed"
        members_by_lid.setdefault(row["lid"], []).extend(group)
        cluster_info.append(
            {
                "lid": row["lid"],
                "event": event,
                "members": [
                    {
                        "reviewer_id": m["_reviewer"],
                        "fid": m["id"],
                        "blocking": bool(m["blocking"]),
                    }
                    for m in group
                ],
            }
        )
    for row in ledger["rows"]:
        if row["status"] == "resolved_check" and row["lid"] not in members_by_lid:
            row["status"] = "resolved"
            row["history"].append({"round": n, "event": "cleared"})
            cleared.append(row["lid"])
    for rid, p in priors:
        try:
            row = _row(ledger, p["prior"])
        except LedgerError:
            warnings.append(f"{rid}: prior line names unknown id {p['prior']}")
            continue
        row["history"].append(
            {
                "round": n,
                "event": "prior_note",
                "reviewer_id": rid,
                "status": p["status"],
            }
        )
    brief = _brief_ids(ledger)
    verdict = "FAIL" if brief else "PASS"
    decision = _decision(ledger, verdict, n)
    ledger["rounds"].append(
        {
            "n": n,
            "doc_sha256": sha256_text(doc_text),
            "reviewers": entries,
            "verdict": verdict,
            "decision": decision,
            "brief_ids": brief,
        }
    )
    return {
        "verdict": verdict,
        "decision": decision,
        "brief_ids": brief,
        "new": new_lids,
        "refound": refound,
        "regressed": regressed,
        "cleared": cleared,
        "clusters": cluster_info,
        "block_ok": block_ok,
        "warnings": warnings,
        "_members": members_by_lid,
    }


def apply_revision(
    ledger: dict, old_text: str, new_text: str, fixmap: Sequence[dict]
) -> dict:
    """Apply a revision: move rows the fix map names as applied (and a hunk touches) to resolved_check; keep spans current."""
    if not ledger["rounds"]:
        raise LedgerError("no review round has been merged yet")
    n = ledger["rounds"][-1]["n"]
    ops = fnd.opcodes(old_text, new_text)
    out: dict[str, list[str]] = {
        "resolved_check": [],
        "named_not_touched": [],
        "rejected": [],
        "unknown": [],
    }
    for item in fixmap:
        try:
            row = _row(ledger, item["id"])
        except LedgerError:
            out["unknown"].append(item["id"])
            continue
        if row["status"] not in ("open", "regressed"):
            continue
        if item["action"] == "applied":
            if fnd.hunks_touch(row.get("span"), ops) or fnd.hunks_touch(
                row.get("span2"), ops
            ):
                row["status"] = "resolved_check"
                row["history"].append({"round": n, "event": "resolved_check"})
                out["resolved_check"].append(row["lid"])
            else:
                row["history"].append({"round": n, "event": "named_not_touched"})
                out["named_not_touched"].append(row["lid"])
        else:
            row["history"].append({"round": n, "event": "rejected_by_reviser"})
            out["rejected"].append(row["lid"])
    for row in ledger["rows"]:
        for key in ("span", "span2"):
            mapped = fnd.map_span(row.get(key), ops)
            row[key] = list(mapped) if mapped else None
    return out


def defer(ledger: dict, lid: str, reason: str) -> None:
    """Human command: park a finding. The stored decision of the last round is recomputed without it."""
    row = _row(ledger, lid)
    row["status"] = "deferred"
    n = ledger["rounds"][-1]["n"] if ledger["rounds"] else 0
    row["history"].append({"round": n, "event": "deferred", "reason": reason})
    if ledger["rounds"]:
        last = ledger["rounds"][-1]
        last["brief_ids"] = [i for i in last.get("brief_ids", []) if i != lid]
        if not last["brief_ids"]:
            last["verdict"], last["decision"] = "PASS", "PASS"


def verdict(ledger: dict) -> dict:
    if not ledger["rounds"]:
        raise LedgerError("no review round has been merged yet")
    last = ledger["rounds"][-1]
    return {
        "verdict": last["verdict"],
        "decision": last["decision"],
        "brief_ids": list(last.get("brief_ids", [])),
        "round": last["n"],
    }


def capture(ledger: dict, n: int, source: str = "") -> dict:
    """Capture matrix (review-capture/1) of one whole-document round."""
    rnd = next((r for r in ledger["rounds"] if r["n"] == n), None)
    if rnd is None:
        raise LedgerError(f"round {n} is not in the ledger")
    occasions = [e["reviewer_id"] for e in rnd["reviewers"]]
    defects = []
    for row in ledger["rows"]:
        members = [m for m in row["members"] if m["round"] == n]
        if not members:
            continue
        by = {m["reviewer_id"] for m in members}
        defects.append(
            {
                "key": row["lid"],
                "blocking": any(m["blocking"] for m in members),
                "captured_by": [o for o in occasions if o in by],
            }
        )
    return {
        "schema": CAPTURE_SCHEMA,
        "source": source,
        "round": n,
        "doc_sha256": rnd["doc_sha256"],
        "occasions": occasions,
        "defects": defects,
    }


def _quote(s: Any) -> str:
    return json.dumps(s, ensure_ascii=False)


def render_merged_report(
    ledger: dict, result: dict, doc_path: str, doc_text: str, n: int
) -> str:
    """The merged report the reviser and the next reviewer read (written by the coordinator script)."""
    rnd = next(r for r in ledger["rounds"] if r["n"] == n)
    cap = ledger["cap_reviews"]
    members = result.get("_members", {})
    out: list[str] = [
        f"review: {n} of {cap}",
        f"# Merged review {n} (coordinator script; panel of {len(rnd['reviewers'])} reviewers)",
        f"candidate: {doc_path} sha256 {sha256_text(doc_text)}",
        "reviewers:",
    ]
    for e in rnd["reviewers"]:
        out.append(
            f"- {e['reviewer_id']}: report {e.get('report')}, block ok {str(e['block_ok']).lower()}"
        )
    out += [
        "",
        "## Ledger",
        "",
        "| lid | status | blocking | confidence | severity | refs | reviewers |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in ledger["rows"]:
        who = sorted({m["reviewer_id"] for m in row["members"]})
        out.append(
            f"| {row['lid']} | {row['status']} | {'yes' if row['blocking'] else 'no'} | {row['confidence']} | {row['severity_max']} | "
            f"{', '.join(row.get('refs') or []) or '-'} | {', '.join(who)} |"
        )
    brief = result["brief_ids"]
    out += ["", "## Blocking findings", ""]
    if not brief:
        out += ["none.", ""]
    for lid in brief:
        row = _row(ledger, lid)
        out += [f"### {lid}", ""]
        cur = members.get(lid, [])
        if cur:
            for m in cur:
                out += [
                    f"#### {lid}.{m['_reviewer']} ({m['id']})",
                    "",
                    f"- claim: {m['claim']}",
                    f"- anchor: {_quote(m['anchor'])}",
                ]
                if m.get("anchor2"):
                    out.append(f"- anchor2: {_quote(m['anchor2'])}")
                out.append("")
        else:
            out += [
                f"#### {lid} (open from an earlier review, not reported again in this one)",
                "",
                f"- claim: {row.get('claim', '')}",
                f"- anchor: {_quote(row['anchor'])}",
            ]
            if row.get("anchor2"):
                out.append(f"- anchor2: {_quote(row['anchor2'])}")
            out.append("")
    out += ["## Other findings", ""]
    others = [r for r in ledger["rows"] if not r["blocking"]]
    if not others:
        out.append("none.")
    for row in others:
        out.append(
            f"- {row['lid']} ({row['severity_max']}, {row['status']}, {row['confidence']}): {row.get('claim', '')}"
        )
    out += ["", "## Reviser brief", ""]
    out.append(
        f"Blocking finding ids: {', '.join(brief)}."
        if brief
        else "Blocking finding ids: none."
    )
    out += ["", REVISER_RULES, "", f"verdict: {result['verdict']}"]
    return "\n".join(out) + "\n"
