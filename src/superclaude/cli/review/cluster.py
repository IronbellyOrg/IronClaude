"""Path-aware clustering of findings-v2 blocks (K4 cluster_v2) and the cluster_agreement telemetry value.

cluster_v2(reviewer_records, snapshot_file_list) is a pure function: it reads its arguments, changes none of them and
returns a JSON-serialisable dict. A reviewer record is (reviewer_id, ordinal, findings_v2_block, calibration_map).

Inputs
- reviewer_id: a non-empty string, unique across records; a record with a duplicate id is skipped and reported.
- ordinal: an integer giving the resolution order; records are processed by (ordinal, input position).
- findings_v2_block: a findings_v2.parse_block result (a dict; valid only when its state is complete and its
  findings is a list) or a bare list of findings (taken as the findings of a valid block). Findings of a block that is
  not valid are not clustered, and the reviewer is not a complete reviewer.
- calibration_map: {finding_id: finding_confidence}, possibly empty or None. A confidence is used only when it is a
  finite number from 0 to 1 (not a bool); a finding with no usable entry has no support value.
- snapshot_file_list: path strings or mappings with a string path (the file_list or files entries of
  artifacts/input-snapshot.yaml). A path matches only by exact string equality.

A malformed record, finding, confidence or snapshot entry is skipped or downgraded and listed in problems; a malformed
citation is counted under citations.malformed. No input shape makes cluster_v2 or clusters_kept raise.

Rules
- Citation tuple (role, path, line_start, line_end): a citation that findings_v2._check_citation rejects is malformed;
  a well-formed citation whose path is not in the snapshot list is unresolved; otherwise it is resolved. Only resolved
  citations take part in span matching.
- Primary citation: the first citation whose role is the reviewed artifact of the finding's lens (plan for
  reflect-pre, source or diff for reflect-post, spec for spec), else the first citation.
- Fingerprint: sha256("v2|" + role + "|" + path + "|" + section + "|" + refs + "|" + class) over the primary
  citation, refs being the comma-joined findings.refs_norm list and class the deviation_class or the empty string.
  section is always the empty string: cluster_v2 receives no document text to take a section from. A finding whose
  primary citation is not resolved has no fingerprint.
- same_defect_v2(a, b): deviation classes compatible (equal, or either is null or none) and refs_norm sets that
  intersect or are both empty and a resolved citation of each on the same path with spans within 3 lines; or equal
  fingerprints with non-empty refs_norm.
- Clusters are union-find components over the findings in resolution order; a cluster is chained when two of its
  members do not match pairwise.
- Reviewer weight w(r): the highest calibrated confidence among the clustered findings of complete reviewer r. The spec
  divides by "the sum of calibrated confidences of all complete reviewers", but confidences exist only per finding, so
  a reviewer's confidence is taken as that of its most confident finding. A complete reviewer with no clustered finding
  (an empty block, or no kept finding in clusters_kept) found nothing and has weight 0.
- support(c) = sum, over the distinct reviewers in c, of the highest calibrated confidence of that reviewer's members
  in c, divided by the sum of w(r) over all complete reviewers. support is at most 1, and is 1 when c holds, for every
  complete reviewer with a clustered finding, a finding of that reviewer at confidence w(r).
- support is None, and the cluster is listed in uncalibrated, when a member has no calibrated confidence. When a
  complete reviewer has clustered findings but none with a calibrated confidence, or the weights sum to 0, the
  denominator is unknown: every cluster has support None and is listed in uncalibrated.
- Representative: the member with the highest calibrated confidence (members with none rank below every calibrated
  one), ties broken by resolution order; it gives the cluster's claim. blocking_any and blocking_all are over all
  members. A cluster is blocking when blocking_any is true.
- disputed: support below 0.5, or members disagree on blocking, or members carry two different non-null
  deviation_class values.
- cluster_agreement: None with fewer than 2 complete reviewers; 1.0 when there is no blocking cluster; otherwise the
  mean support over blocking clusters that are not chained and have a support value, or None when no such cluster
  exists. Chained and uncalibrated clusters are listed.

clusters_kept(reviewer_records, snapshot_file_list, kept) is the second pass: it runs cluster_v2 on copies of the
records holding only the findings whose (reviewer_id, finding id) pair is in kept; block validity is unchanged.
"""

from __future__ import annotations

import hashlib
import math
from typing import Any, Iterable

from superclaude.cli.review.findings import refs_norm
from superclaude.cli.review.findings_v2 import _check_citation

PRIMARY_ROLES = {
    "reflect-pre": ("plan",),
    "reflect-post": ("source", "diff"),
    "spec": ("spec",),
}
SPAN_TOLERANCE = 3


def _str(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _confidence(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    value = float(value)
    return value if math.isfinite(value) and 0 <= value <= 1 else None


def _snapshot(snapshot_file_list: Any, problems: list[dict]) -> set[str]:
    paths: set[str] = set()
    if snapshot_file_list is None:
        return paths
    if isinstance(snapshot_file_list, (str, bytes, dict)) or not isinstance(
        snapshot_file_list, Iterable
    ):
        problems.append({"msg": "snapshot_file_list is not a list of paths"})
        return paths
    for i, entry in enumerate(snapshot_file_list):
        path = entry.get("path") if isinstance(entry, dict) else entry
        if isinstance(path, str) and path:
            paths.add(path)
        else:
            problems.append({"msg": f"snapshot entry {i} has no path string"})
    return paths


def _citation(c: Any, index: int, snapshot: set[str]) -> dict:
    view = {
        "index": index,
        "role": _str(c.get("role")) if isinstance(c, dict) else None,
        "path": _str(c.get("path")) if isinstance(c, dict) else None,
        "line_start": c.get("line_start") if isinstance(c, dict) else None,
        "line_end": c.get("line_end") if isinstance(c, dict) else None,
    }
    if _check_citation(c) is not None:
        view.update(line_start=None, line_end=None, status="malformed")
    else:
        view["status"] = "resolved" if c["path"] in snapshot else "unresolved"
    return view


def _fingerprint(primary: dict, refs: list[str], dclass: str | None) -> str:
    text = "|".join(
        ("v2", primary["role"], primary["path"], "", ",".join(refs), dclass or "")
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def annotate(finding: dict, snapshot: set[str]) -> dict:
    """The view of one finding that same_defect_v2 compares: citations with status, primary, refs_norm, class, fp."""
    raw = finding.get("citations")
    cits = [
        _citation(c, i, snapshot)
        for i, c in enumerate(raw if isinstance(raw, list) else [])
    ]
    roles = PRIMARY_ROLES.get(_str(finding.get("lens")) or "", ())
    primary = next((c for c in cits if c["role"] in roles), cits[0] if cits else None)
    refs = finding.get("refs")
    # refs_norm expects string text fields; a non-string field is left out instead of raising.
    safe: dict[str, Any] = {"refs": refs if isinstance(refs, list) else []}
    for key in ("anchor", "anchor2", "claim"):
        if isinstance(finding.get(key), str):
            safe[key] = finding[key]
    norm = refs_norm(safe)
    dclass = _str(finding.get("deviation_class"))
    fp = (
        _fingerprint(primary, norm, dclass)
        if primary and primary["status"] == "resolved"
        else None
    )
    return {
        "citations": cits,
        "primary_citation": primary,
        "refs_norm": norm,
        "deviation_class": dclass,
        "fp": fp,
    }


def _compatible(a: str | None, b: str | None) -> bool:
    return a == b or a in (None, "none") or b in (None, "none")


def same_defect_v2(a: dict, b: dict) -> bool:
    """True when two annotated findings describe one defect under the rules in the module docstring."""
    if a["fp"] and a["fp"] == b["fp"] and a["refs_norm"]:
        return True
    if not _compatible(a["deviation_class"], b["deviation_class"]):
        return False
    ra, rb = set(a["refs_norm"]), set(b["refs_norm"])
    if not (ra & rb or (not ra and not rb)):
        return False
    for c1 in a["citations"]:
        if c1["status"] != "resolved":
            continue
        for c2 in b["citations"]:
            if (
                c2["status"] == "resolved"
                and c1["path"] == c2["path"]
                and c1["line_start"] <= c2["line_end"] + SPAN_TOLERANCE
                and c2["line_start"] <= c1["line_end"] + SPAN_TOLERANCE
            ):
                return True
    return False


def _records(reviewer_records: Any, problems: list[dict]) -> list[dict]:
    """Valid and invalid reviewer records in resolution order; malformed records are reported and dropped."""
    if isinstance(reviewer_records, (str, bytes, dict)) or not isinstance(
        reviewer_records, Iterable
    ):
        if reviewer_records is not None:
            problems.append({"msg": "reviewer_records is not a list of records"})
        return []
    out = []
    for pos, rec in enumerate(reviewer_records):
        if not isinstance(rec, (list, tuple)) or len(rec) != 4:
            problems.append(
                {
                    "record": pos,
                    "msg": "a record must be (reviewer_id, ordinal, block, calibration_map)",
                }
            )
            continue
        rid, ordinal, block, cal = rec
        if not isinstance(rid, str) or not rid:
            problems.append(
                {"record": pos, "msg": "reviewer_id must be a non-empty string"}
            )
            continue
        if isinstance(ordinal, bool) or not isinstance(ordinal, int):
            problems.append({"record": pos, "msg": "ordinal must be an integer"})
            continue
        if cal is not None and not isinstance(cal, dict):
            problems.append(
                {
                    "record": pos,
                    "msg": "calibration_map is not a mapping; treated as empty",
                }
            )
        if isinstance(block, list):
            findings, valid = block, True
        elif isinstance(block, dict) and isinstance(block.get("findings"), list):
            findings, valid = block["findings"], block.get("state") == "complete"
        else:
            findings, valid = [], False
        out.append(
            {
                "pos": pos,
                "reviewer_id": rid,
                "ordinal": ordinal,
                "findings": findings,
                "valid": valid,
                "cal": cal if isinstance(cal, dict) else {},
            }
        )
    out.sort(key=lambda r: (r["ordinal"], r["pos"]))
    seen: set[str] = set()
    unique = []
    for r in out:
        if r["reviewer_id"] in seen:
            problems.append(
                {
                    "record": r["pos"],
                    "msg": f"duplicate reviewer_id {r['reviewer_id']!r}; record skipped",
                }
            )
            continue
        seen.add(r["reviewer_id"])
        unique.append(r)
    return unique


def _members(
    records: list[dict], snapshot: set[str], problems: list[dict]
) -> list[dict]:
    members = []
    for r in records:
        if not r["valid"]:
            continue
        ids: set[str] = set()
        for i, f in enumerate(r["findings"]):
            fid = f.get("id") if isinstance(f, dict) else None
            if not isinstance(fid, str) or not fid:
                problems.append(
                    {
                        "record": r["pos"],
                        "msg": f"finding {i} has no string id; skipped",
                    }
                )
                continue
            if fid in ids:
                problems.append(
                    {
                        "record": r["pos"],
                        "msg": f"duplicate finding id {fid!r}; skipped",
                    }
                )
                continue
            ids.add(fid)
            conf = None
            if fid in r["cal"]:
                conf = _confidence(r["cal"][fid])
                if conf is None:
                    problems.append(
                        {
                            "record": r["pos"],
                            "msg": f"calibration for {fid!r} is not a number from 0 to 1",
                        }
                    )
            view = annotate(f, snapshot)
            view.update(
                order=len(members),
                reviewer_id=r["reviewer_id"],
                ordinal=r["ordinal"],
                id=fid,
                claim=_str(f.get("claim")) or "",
                blocking=f.get("blocking") is True,
                finding_confidence=conf,
            )
            members.append(view)
    return members


def _components(members: list[dict]) -> list[list[dict]]:
    parent = list(range(len(members)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(members)):
        for j in range(i + 1, len(members)):
            if same_defect_v2(members[i], members[j]):
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[max(ri, rj)] = min(ri, rj)
    groups: dict[int, list[dict]] = {}
    for i, m in enumerate(members):
        groups.setdefault(find(i), []).append(m)
    return [groups[k] for k in sorted(groups)]


def _cluster(index: int, group: list[dict], total: float | None) -> dict:
    chained = any(
        not same_defect_v2(a, b) for i, a in enumerate(group) for b in group[i + 1 :]
    )
    reviewers: list[str] = []
    best: dict[str, float] = {}
    for m in group:
        if m["reviewer_id"] not in reviewers:
            reviewers.append(m["reviewer_id"])
        if m["finding_confidence"] is not None:
            best[m["reviewer_id"]] = max(
                best.get(m["reviewer_id"], 0.0), m["finding_confidence"]
            )
    uncalibrated = total is None or any(m["finding_confidence"] is None for m in group)
    support = None if uncalibrated else sum(best[r] for r in reviewers) / total
    rep = min(
        group,
        key=lambda m: (
            -(m["finding_confidence"] if m["finding_confidence"] is not None else -1.0),
            m["order"],
        ),
    )
    blocking = [m["blocking"] for m in group]
    classes = {m["deviation_class"] for m in group if m["deviation_class"] is not None}
    disputed = (
        (support is not None and support < 0.5)
        or len(set(blocking)) > 1
        or len(classes) > 1
    )
    return {
        "cluster_id": f"C{index}",
        "members": [
            {
                "reviewer_id": m["reviewer_id"],
                "ordinal": m["ordinal"],
                "id": m["id"],
                "blocking": m["blocking"],
                "deviation_class": m["deviation_class"],
                "finding_confidence": m["finding_confidence"],
                "refs_norm": m["refs_norm"],
                "primary_citation": m["primary_citation"],
                "fp": m["fp"],
            }
            for m in group
        ],
        "member_scores": [m["finding_confidence"] for m in group],
        "reviewers": reviewers,
        "chained": chained,
        "uncalibrated": uncalibrated,
        "support": support,
        "representative": {"reviewer_id": rep["reviewer_id"], "id": rep["id"]},
        "claim": rep["claim"],
        "blocking_any": any(blocking),
        "blocking_all": all(blocking),
        "disputed": disputed,
    }


def cluster_v2(reviewer_records: Any, snapshot_file_list: Any) -> dict:
    """Cluster the findings of the valid blocks; see the module docstring for every rule."""
    problems: list[dict] = []
    snapshot = _snapshot(snapshot_file_list, problems)
    records = _records(reviewer_records, problems)
    complete = [r["reviewer_id"] for r in records if r["valid"]]
    members = _members(records, snapshot, problems)
    # A reviewer with no clustered finding found nothing: weight 0.
    weight: dict[str, float] = {r: 0.0 for r in complete}
    calibrated: set[str] = set()
    for m in members:
        if m["finding_confidence"] is not None:
            calibrated.add(m["reviewer_id"])
            weight[m["reviewer_id"]] = max(
                weight[m["reviewer_id"]], m["finding_confidence"]
            )
    with_findings = {m["reviewer_id"] for m in members}
    total = sum(weight.values()) if with_findings <= calibrated else None
    # A weight sum of 0 leaves the denominator unknown, as a missing weight does.
    clusters = [
        _cluster(i, g, total or None) for i, g in enumerate(_components(members), 1)
    ]
    blocking = [c for c in clusters if c["blocking_any"]]
    counted = [c for c in blocking if not c["chained"] and c["support"] is not None]
    if len(complete) < 2:
        agreement = None
    elif not blocking:
        agreement = 1.0
    else:
        agreement = (
            sum(c["support"] for c in counted) / len(counted) if counted else None
        )
    statuses = [c["status"] for m in members for c in m["citations"]]
    return {
        "complete_reviewers": complete,
        "invalid_reviewers": [r["reviewer_id"] for r in records if not r["valid"]],
        "valid_blocks": len(complete),
        "clusters": clusters,
        "cluster_agreement": agreement,
        "blocking_clusters": len(blocking),
        "agreement_clusters": [c["cluster_id"] for c in counted],
        "chained": [c["cluster_id"] for c in clusters if c["chained"]],
        "uncalibrated": [c["cluster_id"] for c in clusters if c["uncalibrated"]],
        "uncalibrated_findings": [
            {"reviewer_id": m["reviewer_id"], "id": m["id"]}
            for m in members
            if m["finding_confidence"] is None
        ],
        "citations": {
            s: statuses.count(s) for s in ("resolved", "unresolved", "malformed")
        },
        "problems": problems,
    }


def _keep(findings: list, rid: Any, pairs: set[tuple[str, str]]) -> list:
    return [
        f
        for f in findings
        if isinstance(rid, str)
        and isinstance(f, dict)
        and isinstance(f.get("id"), str)
        and (rid, f["id"]) in pairs
    ]


def clusters_kept(reviewer_records: Any, snapshot_file_list: Any, kept: Any) -> dict:
    """cluster_v2 over only the findings whose (reviewer_id, finding id) pair is in kept."""
    problems: list[dict] = []
    pairs: set[tuple[str, str]] = set()
    if isinstance(kept, (str, bytes, dict)) or not isinstance(kept, Iterable):
        problems.append(
            {
                "msg": "kept is not a list of (reviewer_id, finding id) pairs; nothing kept"
            }
        )
        kept = []
    for k in kept:
        if (
            isinstance(k, (list, tuple))
            and len(k) == 2
            and all(isinstance(x, str) for x in k)
        ):
            pairs.add((k[0], k[1]))
        else:
            problems.append(
                {"msg": "a kept entry is not a (reviewer_id, finding id) pair"}
            )
    filtered = reviewer_records
    if not isinstance(reviewer_records, (str, bytes, dict)) and isinstance(
        reviewer_records, Iterable
    ):
        filtered = []
        for rec in reviewer_records:
            if isinstance(rec, (list, tuple)) and len(rec) == 4:
                rid, ordinal, block, cal = rec
                if isinstance(block, list):
                    block = _keep(block, rid, pairs)
                elif isinstance(block, dict) and isinstance(
                    block.get("findings"), list
                ):
                    block = {**block, "findings": _keep(block["findings"], rid, pairs)}
                rec = (rid, ordinal, block, cal)
            filtered.append(rec)
    out = cluster_v2(filtered, snapshot_file_list)
    out["problems"].extend(problems)
    return out
