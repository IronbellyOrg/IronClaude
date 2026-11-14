"""collab.json, alarms, audit, anonymiser, results row, arm summary (sections 9 and 10)."""

from __future__ import annotations

import fcntl
import itertools
import json
import math
import re
import statistics
import subprocess
from pathlib import Path

from superclaude.cli.review import findings as F

from . import digest, findings_io, paths, values

_TASK = re.compile(r"^#{1,6}\s+Task\s+(\d+)\b")
_WORD = re.compile(r"[a-z]{3,}")


# ------------------------------------------------------------ 9.2, 9.3


def task_of(candidate: str, anchor: str) -> str | None:
    spans = F.locate(candidate, anchor)
    if not spans:
        return None
    lines = candidate.splitlines()
    for i in range(min(spans[0][0], len(lines) - 1), -1, -1):
        m = _TASK.match(lines[i])
        if m:
            return f"T{m.group(1)}"
    return None


def _jacc(a: set, b: set) -> float | None:
    if not a and not b:
        return None
    return len(a & b) / len(a | b)


def mean_pair_jaccard(sets: dict) -> float | None:
    vals = [
        j
        for x, y in itertools.combinations(sorted(sets), 2)
        if (j := _jacc(sets[x], sets[y])) is not None
    ]
    return sum(vals) / len(vals) if vals else None


def own_line_jaccard(findings_by_rid: dict, candidate: str) -> float | None:
    sets = {
        r: {
            t
            for f in fs
            if f.get("origin", "own") == "own"
            and (t := task_of(candidate, f["anchor"]))
        }
        for r, fs in findings_by_rid.items()
    }
    return mean_pair_jaccard(sets)


def all_line_jaccard(findings_by_rid: dict, candidate: str) -> float | None:
    sets = {
        r: {t for f in fs if (t := task_of(candidate, f["anchor"]))}
        for r, fs in findings_by_rid.items()
    }
    return mean_pair_jaccard(sets)


def _words(s: str) -> set:
    return set(_WORD.findall(s.lower()))


def _common12(a: str, b: str) -> bool:
    a, b = F.flat(a), F.flat(b)
    if len(a) < 12 or len(b) < 12:
        return False
    return any(a[i : i + 12] in b for i in range(len(a) - 11))


def echo_rate(p2_by_rid: dict, slots_by_rid: dict, source_claims: dict):
    """p2_by_rid: rid -> phase-2 findings; slots_by_rid: rid -> digest slots; source_claims: (rid, fid) -> claim."""
    mapped = echoes = 0
    for rid, fs in p2_by_rid.items():
        for f in fs:
            for s in slots_by_rid.get(rid, []):
                if s["slot_type"] != "real" or not _common12(f["anchor"], s["anchor"]):
                    continue
                mapped += 1
                src = source_claims.get((s["source_rid"], s["source_finding_id"]), "")
                if (
                    j := _jacc(_words(f.get("claim", "")), _words(src))
                ) is not None and j > 0.6:
                    echoes += 1
                break
    return "n/a" if mapped == 0 else echoes / mapped


# ------------------------------------------------------------ 9.1

MIDRUN_NULL = [
    "first_delivery_t",
    "stop_blocks",
    "hook_calls",
    "hook_error",
    "hook_ms_p95",
    "snapshot_missing",
    "late",
    "over_cap",
    "finish_signal_t",
]


def _j(p: Path, default=None):
    try:
        return paths.load_json(p)
    except (OSError, json.JSONDecodeError):
        return default


def _events(pkgdir: Path) -> list[dict]:
    return [e for e in findings_io.read_stream(pkgdir / "board" / "events.jsonl")]


def collab_json(pkgdir) -> dict:
    pkgdir = Path(pkgdir)
    pj = paths.load_json(pkgdir / "pkg.json")
    run = paths.load_json(pkgdir.parent / "run.json")
    pc = paths.cfg("panels.json")[pj["panel"]]
    R = digest.roles(pc)
    cand = Path(pj["cand_sb"]).read_text(encoding="utf-8")
    T0 = pj["T0"]
    ev = _events(pkgdir)
    revs, all_f, own_f, p2_f, slots_by, src_claims = {}, {}, {}, {}, {}, {}
    ends = [e["t"] for e in ev if e.get("ev") in ("proc_end",)]
    for rid, role in R.items():
        rv = pkgdir / "reviews"
        meta = _j(rv / f"{rid}.meta.json", {}) or {}
        p2m = _j(rv / f"{rid}.p2.meta.json", {}) or {}
        comb = _j(rv / f"{rid}.combine.json", {}) or {}
        dg = _j(pkgdir / "board" / f"{rid}.digest.json")
        nl = next(
            (
                e.get("reason")
                for e in ev
                if e.get("rid") == rid and e.get("ev") == "no_launch"
            ),
            None,
        )
        revs[rid] = {
            "model": role["model"],
            "msgs_sent": 0,
            "msgs_received": 1 if p2m.get("t_launch") else 0,
            "seal_t": (meta["seal_t"] - T0) if meta.get("seal_t") else None,
            "resume_fallback": bool(p2m.get("resume_fallback", False)),
            "phase2_s": p2m.get("phase2_s"),
            "reask_s": meta.get("reask_s"),
            "p2reask_s": p2m.get("p2reask_s"),
            "attempts": meta.get("attempts"),
            "retry_s": meta.get("retry_s"),
            "retry_isolated": bool(meta.get("retry_isolated", False)),
            "phase2_timeout": bool(p2m.get("phase2_timeout", False)),
            "p2_lines_salvaged": comb.get("p2_lines_salvaged", 0),
            "n_planned": (dg or {}).get("n_planned"),
            "n_launched": p2m.get("n_launched", 0) if p2m else 0,
            "hang_kill": meta.get("state") == "hang_kill",
            "no_launch_reason": nl,
            "output_tokens_all": int(meta.get("output_tokens_all", 0) or 0)
            + int(p2m.get("output_tokens_all", 0) or 0),
            "session_ids": meta.get("session_ids", []) + p2m.get("session_ids", []),
            "state": meta.get("state"),
        }
        for k in MIDRUN_NULL:
            revs[rid][k] = None
        final = rv / f"{rid}.md"
        if final.exists():
            fs = F.parse_block(final.read_text(encoding="utf-8"))["findings"]
            all_f[rid] = fs
            own_f[rid] = [f for f in fs if f.get("origin") == "own"]
            p2_f[rid] = [f for f in fs if f.get("origin") == "peer"]
        p1 = rv / f"{rid}.p1.md"
        if p1.exists():
            for f in digest.load_findings(p1):
                src_claims[(rid, f["id"])] = f.get("claim", "")
        if dg:
            slots_by[rid] = dg["slots"]
    slots = []
    for rid, ss in slots_by.items():
        for s in ss:
            slots.append(
                {
                    "rid": rid,
                    "j": s["j"],
                    "slot_type": s["slot_type"],
                    "move": s["move"],
                    "source_rid": s["source_rid"],
                    "source_finding_id": s["source_finding_id"],
                    "deal_r": s.get("deal_r"),
                    "card_form": None,
                    "deal_c": None,
                }
            )
    vals = pj.get("values", {})
    B = pj["B_f"]
    elapsed = (max(ends) - T0) if ends else None
    crit = (
        [r["rid"] for r in pc["readers"]]
        if pc["critical_role"] == "readers"
        else [pc["searcher"]["rid"]]
    )
    pv = vals.get("pkg", {})
    fin_at = pv.get("panel_finish_offset_s")
    seal_ts = [revs[r]["seal_t"] for r in crit]
    would = bool(fin_at is not None and any(s is None or s > fin_at for s in seal_ts))
    ledger = _j(pkgdir / "merged" / "ledger.json", {}) or {}
    cj = {
        "arm": "A3" if run["collab"] == 1 else "A1",
        "run_id": pj["run_id"],
        "pkg": pj["pkg"],
        "values_sha256": pj.get("values_sha256"),
        "values_status": pj.get("values_status"),
        "reviewers": revs,
        "slots": slots,
        "panel": {
            "T0": T0,
            "elapsed_s": elapsed,
            "baseline_elapsed_s": B,
            "overhead_pct": (elapsed / B - 1) if elapsed is not None else None,
            "k": pv.get("k"),
            "panel_finish_at": fin_at,
            "finish_would_fire": would,
            "slo_breach": bool(pj.get("slo_breach", False)),
            "own_line_jaccard": own_line_jaccard(own_f, cand) if own_f else None,
            "pairwise_task_jaccard": all_line_jaccard(all_f, cand) if all_f else None,
            "echo_rate": echo_rate(p2_f, slots_by, src_claims)
            if run["collab"] == 1
            else "n/a",
            "ledger_rows": len(ledger.get("rows", []))
            if isinstance(ledger.get("rows"), list)
            else None,
            "challenges_real": sum(1 for s in slots if s["slot_type"] == "real"),
            "challenges_gap": sum(1 for s in slots if s["slot_type"] == "gap"),
            "gt_anchor_overlap": None,
        },
    }
    cj["panel"]["panel"] = pj["panel"]
    paths.write_json(pkgdir / "collab.json", cj)
    return cj


# ------------------------------------------------------------ 9.4 audit

FORBIDDEN = [
    "ground-truth",
    "/eval-workspaces/",
    ".dev/reflect",
    "20261113-collab",
    "merged-requirements",
    "/brainstorms/",
    "/.claude/projects/",
]


def _tool_inputs(obj, out: list):
    """Collect JSON-serialised tool_use inputs anywhere in an event structure."""
    if isinstance(obj, dict):
        if obj.get("type") == "tool_use" and "input" in obj:
            out.append(json.dumps(obj["input"], ensure_ascii=False))
        for v in obj.values():
            _tool_inputs(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _tool_inputs(v, out)


def _load_any(p: Path):
    txt = p.read_text(encoding="utf-8", errors="replace")
    try:
        return [json.loads(txt)]
    except json.JSONDecodeError:
        pass
    out = []
    for ln in txt.splitlines():
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out


def audit(pkgdir) -> dict:
    pkgdir = Path(pkgdir)
    pj = paths.load_json(pkgdir / "pkg.json")
    rv = pkgdir / "reviews"
    viol, ignored = [], ""
    repo = Path(pj["sb_pkg"]) / "repo"
    st = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    if st.returncode != 0 or st.stdout.strip():
        viol.append(
            {
                "check": "sandbox_dirty",
                "detail": st.stdout.strip()[:2000] or st.stderr.strip()[:500],
            }
        )
    ig = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "status",
            "--porcelain",
            "--ignored",
            "--untracked-files=all",
        ],
        capture_output=True,
        text=True,
    )
    ignored = ig.stdout.strip()
    for p, key in (
        (Path(pj["cand_sb"]), "cand_sha256"),
        (Path(pj["cand_eval"]), "cand_sha256"),
    ):
        if values.sha256_file(p) != pj[key]:
            viol.append({"check": "candidate_changed", "detail": str(p)})
    files = (
        list(rv.glob("*.json"))
        + list(rv.glob("*.jsonl"))
        + list(rv.glob("sessions/**/*.jsonl"))
    )
    own_copy_prefix = str(Path(pj["sb_pkg"]) / "p1") + "/"
    source_read = {}
    for f in sorted(set(files)):
        if (
            f.name.endswith(".meta.json")
            or f.name.endswith(".cost.json")
            or f.name.endswith(".combine.json")
            or f.name.endswith(".h2.json")
        ):
            continue
        rid = f.name.split(".")[0] if f.parent == rv else None
        if rid is None:
            rid = _rid_of_session(pkgdir, f)
        ins: list[str] = []
        for obj in _load_any(f):
            _tool_inputs(obj, ins)
        forbidden = FORBIDDEN + [str(paths.claude_projects()).rstrip("/") + "/"]
        for s in ins:
            for bad in forbidden:
                if bad in s:
                    viol.append(
                        {
                            "check": "forbidden_read",
                            "file": str(f.relative_to(pkgdir)),
                            "pattern": bad,
                        }
                    )
                    break
            for m in re.finditer(re.escape(own_copy_prefix) + r"[^\s\"']+", s):
                if not (rid and m.group(0).endswith(f"/{rid}.p1.md")):
                    viol.append(
                        {
                            "check": "forbidden_read",
                            "file": str(f.relative_to(pkgdir)),
                            "pattern": m.group(0),
                        }
                    )
            if pj["src_sb"] in s and rid:
                source_read[rid] = True
    for dj in sorted((pkgdir / "board").glob("*.digest*.jsonl")):
        rid = dj.name.split(".")[0]
        pc = paths.cfg("panels.json")[pj["panel"]]
        src = digest.roles(pc)[rid]["sources"]
        cand = Path(pj["cand_sb"]).read_text(encoding="utf-8")
        for ln in dj.read_text(encoding="utf-8").splitlines():
            ok, why = digest.validate_line(ln, cand, rid, src)
            if not ok:
                viol.append({"check": "free_text", "file": dj.name, "reason": why})
    for m in list(rv.glob("*.meta.json")):
        mj = _j(m, {}) or {}
        for sess in mj.get("sessions", []):
            if sess.get("used") and sess.get("model_ok") is False:
                viol.append(
                    {
                        "check": "model_identity",
                        "file": m.name,
                        "session": sess.get("session_id"),
                    }
                )
    # dedupe
    seen, uniq = set(), []
    for v in viol:
        k = json.dumps(v, sort_keys=True)
        if k not in seen:
            seen.add(k)
            uniq.append(v)
    out = {"violations": uniq, "ignored_writes": ignored, "source_read": source_read}
    paths.write_json(pkgdir / "audit.json", out)
    if uniq:
        (pkgdir / "QUARANTINE").write_text(
            "\n".join(json.dumps(v) for v in uniq) + "\n"
        )
    return out


def _rid_of_session(pkgdir: Path, f: Path) -> str | None:
    sid = f.relative_to(pkgdir / "reviews" / "sessions").parts[0]
    for m in (pkgdir / "reviews").glob("*.meta.json"):
        mj = _j(m, {}) or {}
        if sid in (mj.get("session_ids") or []) or sid == mj.get("session_id"):
            return m.name.split(".")[0]
    return None


# ------------------------------------------------------------ 10.1 anonymiser

RESIDUE = [
    "P2-",
    '"origin"',
    "evalsb-collab",
    "20261113-collab",
    "/board/",
    "digest.jsonl",
    "p1norm",
    "/runs/",
    "/reviews/",
]


def anonymise(text: str) -> tuple[str, dict]:
    ids = sorted(set(re.findall(r"\bt[0-9a-z]+-[0-9]+\b", text)))
    for i, rid in enumerate(ids, 1):
        text = re.sub(rf"\b{re.escape(rid)}\b", f"R{i}", text)
    fmap: dict[str, str] = {}

    def fid(old: str) -> str:
        if old not in fmap:
            fmap[old] = f"f{len(fmap) + 1}"
        return fmap[old]

    text = re.sub(
        r"^(####\s+\S+\s+)\(([^)\s]+)\)",
        lambda m: f"{m.group(1)}({fid(m.group(2))})",
        text,
        flags=re.M,
    )
    text = re.sub(r"\bP2X?-F\d+\b", lambda m: fid(m.group(0)), text)
    text = re.sub(
        r"^candidate: \S+ sha256",
        "candidate: <candidate file> sha256",
        text,
        flags=re.M,
    )
    text = re.sub(r"report [^\s,]+", "report <redacted>", text)
    text = re.sub(r"/tmp/evalsb-collab-r3[^\s,)]*", "<sandbox>", text)
    text = re.sub(r',\s*"origin"\s*:\s*"(own|peer)"', "", text)
    text = re.sub(r'"origin"\s*:\s*"(own|peer)"\s*,?\s*', "", text)
    res = [r for r in RESIDUE if r in text]
    if re.search(r"-c[01]-", text):
        res.append("-c[01]-")
    return text, {"reviewers": len(ids), "findings_renamed": len(fmap), "residue": res}


# ------------------------------------------------------------ 10.4 results row

TARGETS = {
    "TASK-WF-designSpec-20261107-075614": {
        "GT1": "B1",
        "GT2": "B2",
        "GT5": "B5",
        "GT6": "I1",
        "GT9": "I4",
        "GT10": "I5",
    },
    "TASK-WF-makeTheAliasOnly-20261105-051649": {"GT1": "B6", "GT3": "B8", "GT4": "I6"},
    "TASK-WF-design-20261108-041415": {"GT1": "I7"},
}
CONTROL = "TASK-WF-design-20261108-041415"


def score_fields(scores: dict, gts: dict) -> dict:
    """scores: pkg -> score.json; gts: pkg -> ground-truth.json."""
    out = {
        "found14": 0,
        "real_blocking8": 0,
        "judge_blocking": 0,
        "wrong_blockers": 0,
        "control_found2": 0,
        "control_wrong_blockers": 0,
        "reach": False,
        "target_hits": [],
    }
    for pkg, s in scores.items():
        if s is None:
            continue
        anyc, blk = (
            set(s.get("gt_covered_any", [])),
            set(s.get("gt_covered_blocking", [])),
        )
        if pkg == CONTROL:
            out["control_found2"] = len(anyc)
            out["control_wrong_blockers"] = int(s.get("wrong_blockers", 0))
        else:
            real = {
                it["id"] for it in gts[pkg]["items"] if it.get("blocking_in_implement")
            }
            out["found14"] += len(anyc)
            out["judge_blocking"] += len(blk)
            out["real_blocking8"] += len(blk & real)
            out["wrong_blockers"] += int(s.get("wrong_blockers", 0))
        for gid, lab in TARGETS.get(pkg, {}).items():
            if gid in anyc:
                out["target_hits"].append(lab)
    out["reach"] = bool(out["target_hits"])
    return out


def _gt_subs(gts: dict) -> list[str]:
    return [
        F.flat(it.get("plan_quote") or "")
        for g in gts.values()
        for it in g["items"]
        if len(F.flat(it.get("plan_quote") or "")) >= 12
    ]


def _has_12(hay: str, quotes: list[str]) -> bool:
    hay = F.flat(hay)
    return any(q[i : i + 12] in hay for q in quotes for i in range(len(q) - 11))


def gt_leak_counts(digest_lines: list[str], gts: dict) -> tuple[int, int]:
    qs = _gt_subs(gts)
    leak = overlap = 0
    for ln in digest_lines:
        try:
            o = json.loads(ln)
        except json.JSONDecodeError:
            continue
        anchor = o.pop("anchor", "")
        if _has_12(json.dumps(o, ensure_ascii=False), qs):
            leak += 1
        if _has_12(anchor, qs):
            overlap += 1
    return leak, overlap


def judge_ok(d: Path) -> bool:
    s = _j(d / "score.json")
    keys = {
        "label",
        "combo",
        "package",
        "gt_total",
        "gt_covered_any",
        "gt_covered_blocking",
        "ledger_rows_total",
        "ledger_rows_blocking",
        "blocking_rows_gt_matched",
        "wrong_blockers",
        "notes",
    }
    if not isinstance(s, dict) or not keys <= set(s):
        return False
    jj = d / "judge.json"
    if not jj.exists():
        return False
    t = jj.read_text(errors="replace")
    return '"is_error":true' not in t.replace(" ", "") and "API Error" not in t


def result_row(rundir) -> dict:
    rundir = Path(rundir)
    run = paths.load_json(rundir / "run.json")
    keys = _j(rundir / "scoring-keys.json", {}) or {}
    pkgs = [p for p in run["pkgs"]]
    gts = {p: paths.load_json(paths.EVAL / p / "ground-truth.json") for p in pkgs}
    scores = {"full": {}, "sealed": {}}
    jok = True
    for k in keys.values():
        d = Path(k["dir"])
        ok = judge_ok(d)
        jok = jok and ok
        scores[k["kind"]][k["pkg"]] = _j(d / "score.json") if ok else None
    invalid, toks_by, elapsed, overhead, slo = [], {}, {}, {}, {}
    contaminated = False
    tot = {
        "challenges_real": 0,
        "challenges_gap": 0,
        "n_planned": 0,
        "n_launched": 0,
        "resume_fallback": 0,
        "phase2_timeout": 0,
        "p2_lines_valid": 0,
        "p2_lines_salvaged": 0,
        "p2_lines_dropped": 0,
        "p2_dupe_dropped": 0,
        "p2_self_reference": 0,
        "retry_isolated": 0,
        "hang_kill": 0,
        "reask_count": 0,
    }
    echo, olj, lrows, fwf = {}, {}, {}, {}
    leak = overlap = 0
    p2tok = reasktok = 0
    for p in pkgs:
        pd = rundir / p
        pj = _j(pd / "pkg.json", {}) or {}
        if not pj.get("valid", False):
            invalid.append(p)
        if (pd / "QUARANTINE").exists():
            contaminated = True
        cj = _j(pd / "collab.json")
        if cj:
            pan = cj["panel"]
            elapsed[p], overhead[p], slo[p] = (
                pan["elapsed_s"],
                pan["overhead_pct"],
                pan["slo_breach"],
            )
            echo[p], olj[p], lrows[p], fwf[p] = (
                pan["echo_rate"],
                pan["own_line_jaccard"],
                pan["ledger_rows"],
                pan["finish_would_fire"],
            )
            tot["challenges_real"] += pan["challenges_real"]
            tot["challenges_gap"] += pan["challenges_gap"]
            toks_by[p] = 0
            for rid, r in cj["reviewers"].items():
                toks_by[p] += r["output_tokens_all"] or 0
                tot["n_planned"] += r["n_planned"] or 0
                tot["n_launched"] += r["n_launched"] or 0
                tot["resume_fallback"] += int(r["resume_fallback"])
                tot["phase2_timeout"] += int(r["phase2_timeout"])
                tot["retry_isolated"] += int(r["retry_isolated"])
                tot["hang_kill"] += int(r["hang_kill"])
                tot["reask_count"] += int(bool(r["reask_s"])) + int(
                    bool(r["p2reask_s"])
                )
                cb = _j(pd / "reviews" / f"{rid}.combine.json", {}) or {}
                for k in (
                    "p2_lines_valid",
                    "p2_lines_salvaged",
                    "p2_lines_dropped",
                    "p2_dupe_dropped",
                    "p2_self_reference",
                ):
                    tot[k] += int(cb.get(k, 0) or 0)
                p2m = _j(pd / "reviews" / f"{rid}.p2.meta.json", {}) or {}
                p2tok += int(p2m.get("output_tokens_all", 0) or 0)
                mj = _j(pd / "reviews" / f"{rid}.meta.json", {}) or {}
                reasktok += int(mj.get("reask_output_tokens", 0) or 0)
        lines = []
        for dj in (pd / "board").glob("*.digest*.jsonl"):
            lines += dj.read_text(encoding="utf-8").splitlines()
        lk, ov = gt_leak_counts(lines, {p: gts[p]})
        leak += lk
        overlap += ov
        if cj:
            cj["panel"]["gt_anchor_overlap"] = ov
            paths.write_json(pd / "collab.json", cj)
    if leak:
        contaminated = True
    full = score_fields(scores["full"], gts)
    row = {
        "schema": "r3-result/1",
        "run_id": run["run_id"],
        "panel": run["panel"],
        "collab": run["collab"],
        "arm": "A3" if run["collab"] == 1 else "A1",
        "values_sha256": run.get("values_sha256"),
        "values_status": run.get("values_status"),
        "smoke": bool(run.get("smoke")),
        "tag": run.get("tag", ""),
        **{
            k: full[k]
            for k in (
                "found14",
                "real_blocking8",
                "judge_blocking",
                "wrong_blockers",
                "control_found2",
                "control_wrong_blockers",
                "reach",
                "target_hits",
            )
        },
        "output_tokens": {
            "total": sum(toks_by.values()),
            "by_pkg": toks_by,
            "phase2": p2tok,
            "reask": reasktok,
        },
        "elapsed_s": elapsed,
        "overhead_pct": overhead,
        "slo_breach": slo,
    }
    if run["collab"] == 1:
        sf = score_fields(scores["sealed"], gts)
        row["sealed"] = {
            k: sf[k]
            for k in (
                "found14",
                "real_blocking8",
                "judge_blocking",
                "wrong_blockers",
                "control_found2",
                "control_wrong_blockers",
                "reach",
            )
        }
        row["collab"] = {
            **tot,
            "echo_rate": echo,
            "own_line_jaccard": olj,
            "ledger_rows": lrows,
            "finish_would_fire": fwf,
            "gt_anchor_overlap": overlap,
            "gt_text_leak": leak,
        }
    else:
        row["sealed"] = {
            k: 0
            for k in (
                "found14",
                "real_blocking8",
                "judge_blocking",
                "wrong_blockers",
                "control_found2",
                "control_wrong_blockers",
            )
        } | {"reach": False}
        row["collab"] = {
            **{k: 0 for k in tot},
            "echo_rate": {p: None for p in pkgs},
            "own_line_jaccard": olj,
            "ledger_rows": lrows,
            "finish_would_fire": fwf,
            "gt_anchor_overlap": overlap,
            "gt_text_leak": leak,
        }
    row["judge_ok"] = bool(jok and keys) if not run.get("no_judge") else False
    row["invalid_pkgs"] = invalid
    row["contaminated"] = contaminated
    paths.write_json(rundir / "result.json", row)
    if run.get("spike4"):
        dest = paths.R3 / "spikes" / "spike4" / "rows.jsonl"
    elif run.get("smoke"):
        dest = paths.results_root() / "smoke.jsonl"
    else:
        dest = paths.results_root() / "results.jsonl"
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(str(dest) + ".lock", "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        with open(dest, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


# ------------------------------------------------------------ 10.5 summary


def fisher_one_sided(a_hits, a_n, b_hits, b_n) -> float:
    """P(X >= b_hits) for the B arm under the hypergeometric null."""
    K, N = a_hits + b_hits, a_n + b_n
    tot = math.comb(N, b_n)
    return (
        sum(
            math.comb(K, x) * math.comb(N - K, b_n - x)
            for x in range(b_hits, min(K, b_n) + 1)
        )
        / tot
    )


def summarize(rows: list[dict], panel: str, b_f: dict | None = None) -> dict:
    rows = [r for r in rows if r.get("panel") == panel]
    for r in rows:
        if r.get("values_status") != "frozen":
            raise SystemExit(
                f"refused: row {r.get('run_id')} values_status={r.get('values_status')}"
            )
    arms = {}
    for arm in ("A1", "A3"):
        rs = [r for r in rows if r["arm"] == arm]
        good = [
            r
            for r in rs
            if not r["invalid_pkgs"] and r["judge_ok"] and not r["contaminated"]
        ]
        m = {}
        for k in (
            "found14",
            "real_blocking8",
            "judge_blocking",
            "wrong_blockers",
            "control_found2",
        ):
            xs = [r[k] for r in good]
            m[k] = {
                "mean": statistics.fmean(xs) if xs else None,
                "min": min(xs) if xs else None,
                "max": max(xs) if xs else None,
            }
        per_pkg = {}
        for r in rs:
            for p, e in r["elapsed_s"].items():
                if e is not None:
                    per_pkg.setdefault(p, []).append(e)
        arms[arm] = {
            "runs": len(rs),
            "quality_runs": len(good),
            "slo_breach": sum(1 for r in rs if any(r["slo_breach"].values())),
            "invalid": sum(1 for r in rs if r["invalid_pkgs"]),
            "judge_not_ok": sum(1 for r in rs if not r["judge_ok"]),
            "contaminated": sum(1 for r in rs if r["contaminated"]),
            "means": m,
            "median_elapsed": {p: statistics.median(v) for p, v in per_pkg.items()},
            "elapsed": per_pkg,
            "reach": sum(1 for r in good if r["reach"]),
            "hard_credits_per_run": statistics.fmean(
                [len(r["target_hits"]) for r in good]
            )
            if good
            else None,
        }
    out = {"panel": panel, "arms": arms}
    a1, a3 = arms["A1"], arms["A3"]
    cap = {}
    for p, b_c in a1["median_elapsed"].items():
        xs = a3["elapsed"].get(p, [])
        cap[p] = {
            "B_c": b_c,
            "median_A3": statistics.median(xs) if xs else None,
            "median_ok": (statistics.median(xs) <= 1.35 * b_c) if xs else None,
            "over_135": sum(1 for x in xs if x > 1.35 * b_c),
            "over_150": sum(1 for x in xs if x > 1.5 * b_c),
        }
    out["cap_check"] = cap
    if b_f:  # baseline_drift = B_c / B_f, band [0.963, 1.10]
        out["baseline_drift"] = {
            p: {"drift": c / b_f[p], "in_band": 0.963 <= c / b_f[p] <= 1.10}
            for p, c in a1["median_elapsed"].items()
            if b_f.get(p)
        }
    a1_rows = [r for r in rows if r["arm"] == "A1"]
    a3_rows = [r for r in rows if r["arm"] == "A3"]
    oj = [
        v
        for r in a1_rows
        for v in (r["collab"].get("own_line_jaccard") or {}).values()
        if isinstance(v, (int, float))
    ]
    lr = [
        v
        for r in a1_rows
        for v in (r["collab"].get("ledger_rows") or {}).values()
        if isinstance(v, (int, float))
    ]
    oj_m = statistics.fmean(oj) if oj else None
    lr_m = statistics.fmean(lr) if lr else None
    conv = 0
    for r in a3_rows:
        ojs = [
            v
            for v in (r["collab"].get("own_line_jaccard") or {}).values()
            if isinstance(v, (int, float))
        ]
        lrs = [
            v
            for v in (r["collab"].get("ledger_rows") or {}).values()
            if isinstance(v, (int, float))
        ]
        if (oj_m is not None and ojs and statistics.fmean(ojs) > oj_m + 0.15) or (
            lr_m and lrs and statistics.fmean(lrs) < 0.8 * lr_m
        ):
            conv += 1
    out["convergence"] = conv
    out["echo"] = sum(
        1
        for r in a3_rows
        for v in (r["collab"].get("echo_rate") or {}).values()
        if isinstance(v, (int, float)) and v > 0.30
    )
    out["fisher_p_reach"] = (
        fisher_one_sided(
            a1["reach"], a1["quality_runs"], a3["reach"], a3["quality_runs"]
        )
        if a1["quality_runs"] and a3["quality_runs"]
        else None
    )
    return out


def summary_table(s: dict) -> str:
    lines = [
        "| Arm | runs | quality runs | found14 mean | real_blocking8 mean | wrong_blockers mean | reach | SLO breach | invalid | contaminated |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for arm, a in s["arms"].items():
        m = a["means"]
        lines.append(
            f"| {arm} | {a['runs']} | {a['quality_runs']} | {m['found14']['mean']} | {m['real_blocking8']['mean']} | "
            f"{m['wrong_blockers']['mean']} | {a['reach']} | {a['slo_breach']} | {a['invalid']} | {a['contaminated']} |"
        )
    return "\n".join(lines)


# ------------------------------------------------------------ 9.5 transcript capture


def _session_ids(pkgdir: Path) -> set:
    rv = pkgdir / "reviews"
    ids = set()
    for m in rv.glob("*.json"):
        j = _j(m)
        if isinstance(j, dict):
            if isinstance(j.get("session_id"), str) and j["session_id"]:
                ids.add(j["session_id"])
            ids.update(s for s in (j.get("session_ids") or []) if s)
        elif isinstance(j, list):
            ids.update(
                e.get("session_id")
                for e in j
                if isinstance(e, dict) and e.get("session_id")
            )
    for s in list(rv.glob("*.stream.jsonl")):
        ids.update(
            e.get("session_id")
            for e in findings_io.read_stream(s)
            if e.get("session_id")
        )
    return {i for i in ids if i}


def _first_entry(p: Path):
    try:
        with open(p, encoding="utf-8", errors="replace") as fh:
            for ln in fh:
                try:
                    return json.loads(ln)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return None
    return None


def _first_user_text(p: Path) -> str | None:
    try:
        with open(p, encoding="utf-8", errors="replace") as fh:
            for ln in fh:
                try:
                    e = json.loads(ln)
                except json.JSONDecodeError:
                    continue
                if e.get("type") == "user":
                    c = (e.get("message") or {}).get("content")
                    if isinstance(c, str):
                        return c
                    if isinstance(c, list):
                        return "".join(
                            x.get("text", "") for x in c if isinstance(x, dict)
                        )
                    return None
    except OSError:
        return None
    return None


def capture_sessions(pkgdir) -> dict:
    """Copy every transcript file of the package's sessions into reviews/sessions/<id>/ (9.5)."""
    pkgdir = Path(pkgdir)
    rv = pkgdir / "reviews"
    root = paths.claude_projects()
    ids = _session_ids(pkgdir)
    pj = paths.load_json(pkgdir / "pkg.json")
    # killed json attempts: recover the id from the slug directory by time window and brief
    for am in rv.glob("*.attempt*.meta.json"):
        m = _j(am, {}) or {}
        if m.get("session_id") or not m.get("t_start"):
            continue
        rid = am.name.split(".")[0]
        brief_f = rv / f"{rid}.brief.txt"
        brief = (
            brief_f.read_text(encoding="utf-8").strip() if brief_f.exists() else None
        )
        for cand in root.glob("*/*.jsonl"):
            fe = _first_entry(cand)
            ts = (fe or {}).get("timestamp")
            if not isinstance(ts, str):
                continue
            try:
                t = values._ts(ts)
            except ValueError:
                continue
            if m["t_start"] - 1 <= t <= (m.get("t_end") or t) + 1:
                ut = _first_user_text(cand)
                if brief is None or (ut is not None and ut.strip() == brief):
                    ids.add(cand.stem)
                    m.setdefault("recovered_session_ids", []).append(cand.stem)
        paths.write_json(am, m)
    manifest = []
    import shutil

    for sid in sorted(ids):
        for f in root.glob(f"*/{sid}.jsonl"):
            dest = rv / "sessions" / sid / f.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
            manifest.append(str(f))
        for d in root.glob(f"*/{sid}"):
            if d.is_dir():
                for f in d.rglob("*"):
                    if f.is_file():
                        dest = rv / "sessions" / sid / f.relative_to(d.parent)
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(f, dest)
                        manifest.append(str(f))
    (rv / "sessions").mkdir(exist_ok=True)
    (rv / "sessions" / "manifest.txt").write_text("".join(m + "\n" for m in manifest))
    return {"ids": sorted(ids), "files": len(manifest), "run_id": pj["run_id"]}
