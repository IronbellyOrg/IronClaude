"""Poll loop that turns scout exits into coverage cards (DESIGN 2.3). No model sends anything; the watcher authors every card."""
import argparse
import fcntl
import json
import os
import re
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

from superclaude.cli.review.findings import parse_block

from r5 import append_jsonl, h2, now_ms, read_json
from r5 import coverage as cov
from r5.panelmsg import Ctx, candidate_tasks, validate

META = re.compile(r"^(?P<rid>.+)\.attempt(?P<n>\d+)\.meta\.json$")


def post(board: Path, line: str) -> None:
    """Write the card to a temp file in board/, then append it under flock board/msgs/.lock."""
    fd, tmp = tempfile.mkstemp(dir=board, prefix=".card-")
    with os.fdopen(fd, "w") as f:
        f.write(line + "\n")
    with open(board / "msgs" / ".lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        with open(board / "msgs" / "watcher.jsonl", "a") as out_, open(tmp) as src:
            out_.write(src.read())
    os.unlink(tmp)


def run(a) -> int:
    d = Path(a.run_dir)
    board, rev = d / "board", d / "reviews"
    info = read_json(d / "run.json")
    scouts = info["scouts"]
    receivers = info["receivers"]
    cand = Path(a.candidate).read_text()
    index = cov.task_index(cand)
    tasks = [t for t, _s, _e in index]
    pattern = cov.surface_pattern()
    ctx = Ctx(candidate_tasks(cand), set(receivers), a.k, f"{a.row}/{a.pkg}")
    log = board / "watcher.log"
    seen: set[str] = set()
    final: set[str] = set()
    findings: list = []
    declared: Counter = Counter()
    prev: dict = {}
    nposted: Counter = Counter()

    def ev(**kw):
        append_jsonl(log, {"t": now_ms(), **kw})

    ev(event="start", scouts=scouts, receivers=receivers, k=a.k, finish_ms=a.finish_ms)
    while True:
        for p in sorted(rev.glob("*.attempt*.meta.json")):
            m = META.match(p.name)
            if not m or m["rid"] not in scouts or p.name in seen:
                continue
            seen.add(p.name)
            rid, n = m["rid"], int(m["n"])
            meta = read_json(p) or {}
            usable = meta.get("model_ok") is True and meta.get("findings_block") is True and meta.get("api_error") is False
            if usable or n >= 2:
                final.add(rid)
            if not usable:
                ev(event="scout_unusable", rid=rid, attempt=n)
                continue
            try:
                report = (rev / f"{rid}.attempt{n}.md").read_text(errors="replace")
            except OSError:
                ev(event="scout_unusable", rid=rid, attempt=n, reason="report missing")
                continue
            text, _errs = h2.normalise(report)
            found = parse_block(text)["findings"]
            for f in found:
                append_jsonl(board / "coverage.jsonl", {
                    "rid": rid, "attempt": n, "fid": f.get("id"), "category": f.get("category"),
                    "tasks": sorted(cov.tasks_of(f, cand, index)), "surface": cov.is_surface(f, pattern)})
            if not found:
                ev(event="no_findings", rid=rid, attempt=n)
            findings.extend(found)
            declared.update(cov.declared_not_checked(report))
            t = now_ms()
            if t >= a.finish_ms:
                ev(event="after_finish", rid=rid, attempt=n)
                continue
            if a.k <= 0:
                ev(event="k0", rid=rid)
                continue
            covered = cov.covered(findings, cand, index, pattern)
            uncovered = set(tasks) - covered
            ranked = cov.rank(uncovered, {t_: declared[t_] for t_ in uncovered if declared[t_]}, a.row, a.pkg)
            ev(event="rank", after=rid, covered=sorted(covered), rank=ranked)
            for to, (items, status) in cov.next_card(prev, ranked, uncovered, a.k, receivers, a.deal_r).items():
                if items is None:
                    ev(event=status, to=to, after=rid)
                    continue
                nposted[to] += 1
                card = {"v": "panel-msg/1", "id": f"c-{to}-{nposted[to]}", "run": f"{a.row}/{a.pkg}", "from": "watcher",
                        "to": to, "t": now_ms(), "kind": "coverage", "items": items}
                line = json.dumps(card, separators=(",", ":"))
                ok, why = validate(line, ctx)
                if not ok:
                    append_jsonl(board / "rejected.jsonl", {"line": line, "reason": why})
                    nposted[to] -= 1
                    continue
                post(board, line)
                prev[to] = items
                ev(event="posted", id=card["id"], to=to, items=items)
        if set(scouts) <= final or now_ms() >= a.finish_ms:
            ev(event="exit", final=sorted(final))
            return 0
        time.sleep(a.poll)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="r5.watcher")
    for x in ("--run-dir", "--candidate", "--panel", "--row", "--pkg"):
        ap.add_argument(x, required=True)
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--finish-ms", type=int, required=True)
    ap.add_argument("--deal-r", type=int, default=0)
    ap.add_argument("--poll", type=float, default=2.0)
    return run(ap.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
