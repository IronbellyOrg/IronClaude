"""Contamination and read-only audit (DESIGN 2.10; R-07, R-09, MR:970). Output is ids only, never ground-truth text."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from superclaude.cli.review.findings import flat

from r5 import PKGS, cfg, eval_dir, out, read_json, read_jsonl, sb, write_json
from r5 import coverage as cov
from r5.panelmsg import Ctx, candidate_tasks, validate

FORBIDDEN = (".dev/reflect", "ground-truth", "20261111-a1", "20261113-collab", "/board/", "r5-coverage-deflection",
             ".claude/projects", "/home/coder/workspaces/worktrees/IronClaude")
PATH_TOKEN = re.compile(r"[\w.-]+(?:/[\w.-]+)+|[\w-]+\.(?:py|md|json|sh|ya?ml|txt|toml)\b")


def gt_items(gt_files=None) -> list[tuple[str, dict]]:
    files = gt_files or [eval_dir() / p / "ground-truth.json" for p in PKGS]
    items = []
    for f in files:
        g = read_json(f)
        if g:
            items += [(f"{Path(f).parent.name}:{i['id']}", i) for i in g.get("items", [])]
    return items


def _windows(s: str) -> set[str]:
    t = flat(s)
    return {t[i:i + 12] for i in range(len(t) - 11)}


def historical_brief_windows() -> set[str]:
    """12-character windows of the A1 brief of run-reviewer.sh:13-17, which every historical run already carried.

    Deviation from DESIGN 2.10 (recorded in IMPLEMENTATION.md): brief-a1.txt must stay byte-identical to that brief
    (R-05), and it shares generic phrases such as "or when the" with a plan_quote; text inherited from the historical
    brief carries no ground-truth information, so its windows are exempt from the R-07 window check.
    """
    try:
        lines = (eval_dir() / "tools" / "run-reviewer.sh").read_text().split("\n")[12:17]
    except OSError:
        return set()
    return _windows("\n".join(lines))


def leaks(text: str, items, exempt: set[str] = frozenset()) -> list[str]:
    """Ids of ground-truth items that share a 12-character window of a plan_quote, or a description path, with text."""
    windows = _windows(text) - exempt
    hits = []
    for gid, it in items:
        q = flat(it.get("plan_quote") or "")
        if any(q[i:i + 12] in windows for i in range(len(q) - 11)):
            hits.append(f"{gid}:plan_quote")
        for path in set(PATH_TOKEN.findall(it.get("description") or "")):
            if "/" in path or "." in path:
                if path in text:
                    hits.append(f"{gid}:path")
                    break
    return hits


def static_files() -> list[Path]:
    c = cfg()
    return [c / "catalogue.md", c / "surface.regex"] + sorted((c / "templates").glob("*.txt"))


def static(gt_files=None) -> dict:
    items = gt_items(gt_files)
    exempt = historical_brief_windows()
    viol = {str(p.name): leaks(p.read_text(), items, exempt) for p in static_files()}
    viol = {k: v for k, v in viol.items() if v}
    return {"ok": not viol and bool(items), "violations": viol, "gt_items": len(items)}


def tool_inputs(path: Path) -> list[str]:
    """Tool-use inputs of the main session and subagents, from a json array, a jsonl session or a stream-json file."""
    objs = []
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return []
    try:
        x = json.loads(text)
        objs = x if isinstance(x, list) else [x]
    except ValueError:
        objs = [o for o in (_try(line) for line in text.splitlines()) if o]
    out_ = []
    for o in objs:
        msg = o.get("message") if isinstance(o, dict) else None
        for part in (msg or {}).get("content") or [] if isinstance(msg, dict) else []:
            if isinstance(part, dict) and part.get("type") == "tool_use":
                out_.append(json.dumps(part.get("input"), ensure_ascii=False))
    return out_


def _try(line):
    try:
        return json.loads(line)
    except ValueError:
        return None


def package(run_dir) -> dict:
    d = Path(run_dir)
    info = read_json(d / "run.json")
    pkg = info["pkg"]
    checks = {}
    items = gt_items()
    board = d / "board"
    # board text and no free text
    if board.is_dir():
        cand = (sb() / "cand" / pkg / "candidate.md").read_text()
        ctx = Ctx(candidate_tasks(cand), set(info["receivers"]), info["k"], f"{info['row']}/{pkg}")
        msgs = (board / "msgs" / "watcher.jsonl").read_text().splitlines() if (board / "msgs" / "watcher.jsonl").exists() else []
        bad = [i for i, line in enumerate(msgs) if line.strip() and not validate(line, ctx)[0]]
        checks["no_free_text"] = {"ok": not bad, "bad_lines": bad}
        cards = {json.loads(m)["id"]: json.loads(m) for m in msgs if m.strip() and _try(m)}
        text_bad, leak = [], []
        for rid in info["receivers"]:
            for x in read_jsonl(board / "delivered" / f"{rid}.jsonl"):
                if x.get("status") != "delivered" or x["id"] not in cards:
                    continue
                txt = cov.render_card(cards[x["id"]]["items"], info["k"], x.get("template") == "card-2.txt")
                if hashlib.sha256(txt.encode()).hexdigest() != x.get("text_sha256"):
                    text_bad.append(x["id"])
                leak += leaks(txt, items)
        leak += leaks("\n".join(msgs), items)
        checks["board_text"] = {"ok": not text_bad and not leak, "sha_mismatch": text_bad, "gt_hits": sorted(set(leak))}
    # transcripts
    hits = []
    for f in sorted((d / "reviews").glob("*")):
        if f.name.endswith((".attempt1.json", ".attempt2.json", ".session.jsonl", ".reask.jsonl")):
            for inp in tool_inputs(f):
                for s in FORBIDDEN:
                    if s in inp:
                        hits.append({"file": f.name, "pattern": s})
    checks["transcripts"] = {"ok": not hits, "hits": hits[:50]}
    # read-only
    repo = sb() / pkg / "repo"
    st = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True)
    man = (read_json(sb() / "manifest.json") or {}).get(pkg, {})
    def sha(p):
        try:
            return hashlib.sha256(Path(p).read_bytes()).hexdigest()
        except OSError:
            return None
    sums_ok = (sha(sb() / "cand" / pkg / "candidate.md") == man.get("candidate_sha256")
               and sha(sb() / "cand" / pkg / "source.md") == man.get("source_sha256") and bool(man))
    checks["read_only"] = {"ok": st.returncode == 0 and not st.stdout.strip() and sums_ok,
                           "git_status_lines": len(st.stdout.splitlines()), "git_rc": st.returncode, "sums_ok": sums_ok}
    # model
    mbad = []
    for rid, model in info["models"].items():
        m = read_json(d / "reviews" / f"{rid}.meta.json") or {}
        if not m.get("model_ok") or m.get("expected_model") != model or (m.get("reask_used") and not m.get("reask_model_ok")):
            mbad.append(rid)
    checks["model"] = {"ok": not mbad, "bad": mbad}
    status = "pass" if all(c["ok"] for c in checks.values()) else "quarantined"
    res = {"status": status, "checks": checks}
    write_json(d / "audit.json", res)
    return res


def main(argv: list[str]) -> int:
    if argv[0] == "static":
        r = static()
    elif argv[0] == "package":
        r = package(argv[1])
        r = {"status": r["status"], "ok": r["status"] == "pass"}
    elif argv[0] == "row":
        rs = {p.name: package(p)["status"] for p in sorted((out() / "runs" / argv[1]).iterdir()) if (p / "run.json").exists()}
        r = {"ok": all(v == "pass" for v in rs.values()), "packages": rs}
    else:
        return 2
    print(json.dumps(r))
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
