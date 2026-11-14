"""Contamination, read-only and catalogue audits (DESIGN 2.8, R-07, R-09).

audits.py run --pkgdir runs/<row>/<pkg> [--gt <ground-truth.json> ...]   -> writes <pkgdir>/audit.json; exit 1 on violation
audits.py catalogue [--gt <ground-truth.json> ...]                        -> exit 1 on violation (Gate 0)

Only tool INPUTS of assistant entries are audited (Read file_path, Bash command, Grep/Glob path and pattern).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import R2  # noqa: E402

SBR = os.environ.get("R2_SBR", "/tmp/evalsb-collab-r2")
EVAL_PKGS = json.loads((R2 / "config/panels.json").read_text())["packages"]


PATH_TOKEN = re.compile(r"[\w.@+-]*(?:/[\w.@+-]+)+/?(?::\d+)?")


def flat(s: str) -> str:
    return " ".join((s or "").split())


def windows(quotes: list[str], n: int = 12) -> set[str]:
    out = set()
    for q in quotes:
        q = flat(q)
        out |= {q[i:i + n] for i in range(len(q) - n + 1)}
    return out


def gt_hit(text: str, wins: set[str], n: int = 12) -> str | None:
    t = flat(text)
    for i in range(len(t) - n + 1):
        if t[i:i + n] in wins:
            return t[i:i + n]
    return None


def load_gt(paths: list[str]) -> list[dict]:
    items = []
    for p in paths:
        items += json.loads(Path(p).read_text()).get("items", [])
    return items


def tool_inputs(entries) -> list[tuple[str, str]]:
    out = []
    for e in entries if isinstance(entries, list) else []:
        if e.get("type") != "assistant":
            continue
        for c in (e.get("message") or {}).get("content") or []:
            if not isinstance(c, dict) or c.get("type") != "tool_use":
                continue
            inp = c.get("input") or {}
            for key in ("file_path", "command", "path", "pattern"):
                if isinstance(inp.get(key), str):
                    out.append((c.get("name", ""), inp[key]))
    return out


def load_transcript(p: Path):
    try:
        if p.suffix == ".jsonl":
            return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
        return json.loads(p.read_text())
    except (OSError, json.JSONDecodeError):
        return []


def path_violation(value: str, who: str, own_post: str | None) -> str | None:
    if who == "sweeper" and own_post and own_post in value:
        return None
    rules = [(r"ground-truth[^/\s'\"]*\.json", "ground_truth"), (r"20261111-a1", "eval_dir"),
             (r"20261113-collab", "collab_dir"), (r"\.dev/reflect(/|\b)", "reflect")]
    if who == "reviewer":
        rules.append((re.escape(SBR.rstrip("/") + "/board"), "board"))
    else:
        rules += [(r"/reviews/", "reviews_dir"), (re.escape(str(R2 / "runs")), "runs_dir")]
    for rx, name in rules:
        if re.search(rx, value):
            return name
    return None


def sha(p: Path) -> str | None:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def run(pkgdir: Path, gt_paths: list[str]) -> dict:
    v = []
    inputs = json.loads((pkgdir / "inputs.json").read_text())
    sb = Path(inputs["sandbox"])
    sandbox_rules = ("read_only", "candidate_changed", "source_changed")
    prev_path = pkgdir / "audit.json"
    prev = json.loads(prev_path.read_text()) if prev_path.exists() else None
    carried = False
    if not sb.exists() and prev is not None:
        # the sandbox lives under /tmp and is gone: re-auditing an old package keeps the sandbox verdicts recorded while it existed
        carried = True
        v += [x for x in prev.get("violations", []) if x.get("rule") in sandbox_rules]
    else:
        st = subprocess.run(["git", "-C", str(sb / "repo"), "status", "--porcelain"], capture_output=True, text=True)
        if st.returncode != 0 or st.stdout.strip():
            v.append({"rule": "read_only", "detail": (st.stdout or st.stderr)[:500]})
        if sha(sb / "cand/candidate.md") != inputs["candidate_sha256"]:
            v.append({"rule": "candidate_changed"})
        if sha(sb / "cand/source.md") != inputs["source_sha256"]:
            v.append({"rule": "source_changed"})
    board = pkgdir / "board"
    # the sweeper's calls of its own B/bin/panel-post are exempt (DESIGN 2.8)
    post_path = None
    if (board / "conf.json").exists():
        run_id = json.loads((board / "conf.json").read_text())["run"]
        post_path = f"{SBR.rstrip('/')}/board/{run_id}/bin/panel-post"
    for p in sorted((pkgdir / "reviews").glob("*.attempt*.json")) + sorted((pkgdir / "reviews").glob("*.reask.jsonl")):
        for tool, val in tool_inputs(load_transcript(p)):
            why = path_violation(val, "reviewer", None)
            if why:
                v.append({"rule": f"reviewer_read:{why}", "file": p.name, "tool": tool, "value": val[:300]})
    swp = pkgdir / "sweeper/sw-1.json"
    for tool, val in tool_inputs(load_transcript(swp)):
        why = path_violation(val, "sweeper", post_path)
        if why:
            v.append({"rule": f"sweeper_read:{why}", "tool": tool, "value": val[:300]})
    if gt_paths:
        wins = windows([it.get("plan_quote", "") for it in load_gt(gt_paths)])
        texts = []
        notes = []
        for line in ((board / "msgs/board.jsonl").read_text().splitlines() if (board / "msgs/board.jsonl").exists() else []):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                texts.append(("board", line))
                continue
            for key, val in obj.items():
                text = " ".join(map(str, val)) if isinstance(val, list) else str(val)
                # deviation from DESIGN 2.8: an anchor is validator-checked plan text and ground-truth quotes are plan
                # text too, so a 12-character overlap (e.g. " `tests/skil") is chance, not a leak; recorded as a note
                if key == "anchor":
                    hit = gt_hit(text, wins)
                    if hit:
                        notes.append({"rule": "anchor_gt_overlap", "id": obj.get("id"), "hit": hit})
                else:
                    # likewise a repo path (tests/skills/x.py) is a coordinate, not ground-truth prose: the sweeper is meant to
                    # find the very files a ground-truth quote names; only the prose around the paths is audited
                    texts.append((f"board.{key}", PATH_TOKEN.sub(" ", text)))
        # fix 2026-11-14 (owner: "fix design 2"): the A1 brief is the shared, sha256-pinned harness brief that the isolated baseline
        # arm uses too. Ordinary English in it can match a plan quote by chance (", or when th" matched designSpec GT3 and marked that
        # package invalid in every row, both arms). Same reasoning as the anchor note above: a 12-character overlap is a note; only a
        # long overlap (40 characters or more) would be ground-truth prose in the brief, and that stays a violation.
        brief = (R2 / "config/brief-a1.tmpl").read_text()
        quotes = [it.get("plan_quote", "") for it in load_gt(gt_paths)]
        long_hit = gt_hit(brief, windows(quotes, 40), 40)
        if long_hit:
            v.append({"rule": "ground_truth_text", "where": "brief_a1", "hit": long_hit})
        elif gt_hit(brief, wins):
            notes.append({"rule": "brief_gt_overlap", "where": "brief_a1", "hit": gt_hit(brief, wins)})
        texts += [("sweeper_brief", (R2 / "config/sweeper-brief.tmpl").read_text()),
                  ("catalogue", (R2 / "config/catalogue.json").read_text())]
        # a rendered delivery is the fixed template + catalogue text + the board line's fields: covered above
        for where, t in texts:
            hit = gt_hit(t, wins)
            if hit:
                v.append({"rule": "ground_truth_text", "where": where, "hit": hit})
    res = {"ok": not v, "violations": v, "gt_checked": bool(gt_paths)}
    if carried:
        res["sandbox_checks"] = "carried-from-previous-audit"
    if gt_paths and notes:
        res["notes"] = notes
    (pkgdir / "audit.json").write_text(json.dumps(res, indent=1) + "\n")
    return res


def catalogue(gt_paths: list[str]) -> dict:
    items = load_gt(gt_paths)
    text = json.dumps(json.loads((R2 / "config/catalogue.json").read_text())["moves"], ensure_ascii=False)
    v = []
    hit = gt_hit(text, windows([it.get("plan_quote", "") for it in items]))
    if hit:
        v.append({"rule": "plan_quote_substring", "hit": hit})
    paths = set()
    for it in items:
        paths |= {t.strip("`'\"(),.;:") for t in re.findall(r"[\w./-]+", it.get("description", ""))
                  if "/" in t or re.search(r"\.(py|md|json|sh|yaml|yml|toml)\b", t)}
    for p in sorted(paths):
        if len(p) >= 4 and p in text:
            v.append({"rule": "gt_path_in_catalogue", "path": p})
    return {"ok": not v, "violations": v, "gt_files": gt_paths}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--pkgdir", required=True)
    r.add_argument("--gt", nargs="*", default=[])
    c = sub.add_parser("catalogue")
    c.add_argument("--gt", nargs="*", default=None)
    a = ap.parse_args(argv)
    if a.cmd == "run":
        res = run(Path(a.pkgdir), a.gt)
    else:
        ev = Path(os.environ.get("R2_EVAL") or R2.parents[1] / "20261111-a1")
        gts = a.gt if a.gt is not None else [str(ev / p / "ground-truth.json") for p in EVAL_PKGS]
        res = catalogue(gts)
    print(json.dumps(res))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
