#!/usr/bin/env python3
"""O2/O3: replay the recorded Stage 2 arm-3 loops through `superclaude review merge` / `ledger revise`.

k=1: one reviewer (the recorded report plus its hand-written findings block). k=2: the same report twice.
Compares the ledger decision sequence with the baseline verdict sequence.
"""
import json, pathlib, re, shutil, subprocess, sys

SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
CLONE = SP / "p13/clones/pn1"
AB = SP / "p13/ab1"
OV = SP / "exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md"
CLI = ["uv", "run", "--project", str(CLONE), "superclaude", "review"]
BASELINE = {"a3-r1": ["FAIL", "PASS"], "a3-r2": ["FAIL", "PASS"], "a3-r3": ["FAIL", "PASS"], "a3-r4": ["FAIL", "PASS"],
            "a3-r5": ["FAIL", "PASS"], "a3-r6": ["FAIL", "FAIL", "PASS"]}


def cli(*args, ok=(0,)):
    r = subprocess.run([*CLI, *map(str, args)], capture_output=True, text=True)
    if r.returncode not in ok:
        raise SystemExit(f"CLI failed {args}: {r.returncode}\n{r.stdout}\n{r.stderr}")
    return r


def block(lines):
    return "\n\n## Findings block\n\n```findings-v1\n" + "".join(l.rstrip("\n") + "\n" for l in lines) + "```\n"


def replay(run, k, wd):
    runs = SP / "p11/runs" / run / "ws/.dev/orca-command-refactor"
    hist = runs / "specs/history"
    final = runs / "specs/orca-worker-contract-spec.md"
    versions = {1: OV}
    if (hist / "spec-v2.md").exists():
        versions[2] = hist / "spec-v2.md"
        versions[3] = final
        after = {1: hist / "spec-v2.md", 2: final}
    else:
        versions[2] = final
        after = {1: final}
    n_rounds = 3 if (hist / "spec-v2.md").exists() else 2
    wd.mkdir(parents=True, exist_ok=True)
    ledger = wd / "ledger.json"
    res_first = wd / "panel.json"
    ids = [f"t1b-{1}"] + (["t2-1"] if k == 2 else [])
    res_first.write_text(json.dumps({"reviewers": [{"reviewer_id": i, "model": "replay"} for i in ids]}))
    fid2lid = {}
    seq = []
    log = []
    cur_old = OV
    for n in range(1, n_rounds + 1):
        lines = [json.loads(x) for x in (AB / "fixtures" / run / f"round{n}.findings").read_text().splitlines() if x.strip()]
        out_lines = []
        for ln in lines:
            if "prior" in ln:
                ln = dict(ln, prior=fid2lid.get(ln["prior"], ln["prior"]))
            out_lines.append(json.dumps(ln))
        report = (runs / "review" / f"round{n}.md").read_text() + block(out_lines)
        args = ["merge", "--ledger", ledger, "--doc", versions[n], "--round", n, "--resolution", res_first, "--out", wd / f"round{n}.merged.md"]
        for rid in ids:
            rp = wd / f"round{n}-{rid}.md"
            rp.write_text(report)
            args += ["--report", f"{rid}={rp}"]
        out = json.loads(cli(*args).stdout)
        seq.append(out["decision"] if out["decision"] != "ESCALATE" else "FAIL")
        verdict = out["verdict"]
        log.append({"round": n, "verdict": verdict, "decision": out["decision"], "brief_ids": out["brief_ids"], "new": out["new"],
                    "refound": out["refound"], "regressed": out["regressed"], "cleared": out["cleared"], "block_ok": out["block_ok"],
                    "warnings": out["warnings"]})
        led = json.loads(ledger.read_text())
        for row in led["rows"]:
            for m in row["members"]:
                fid2lid[m["fid"]] = row["lid"]
        if out["decision"] != "REVISE":
            break
        fm = [{"id": lid, "action": "applied", "reason": "recorded revision"} for lid in out["brief_ids"]]
        fmp = wd / f"revise{n}.md"
        fmp.write_text("## Fix map\n\n```fixmap-v1\n" + "\n".join(json.dumps(i) for i in fm) + "\n```\n")
        rv = json.loads(cli("ledger", "revise", "--ledger", ledger, "--old", versions[n], "--new", after[n], "--fixmap", fmp).stdout)
        log[-1]["revise"] = rv
    base = BASELINE[run]
    got = ["PASS" if (x == "PASS") else "FAIL" for x in seq]
    return {"run": run, "k": k, "decisions": got, "baseline": base, "match": got == base, "log": log,
            "rows": [(r["lid"], r["status"], r["confidence"], len(r["members"])) for r in json.loads(ledger.read_text())["rows"]]}


def main():
    root = AB / "offline/replay"
    if root.exists():
        shutil.rmtree(root)
    results = {}
    for k in (1, 2):
        for run in sorted(BASELINE):
            results[f"{run}/k{k}"] = replay(run, k, root / f"k{k}" / run)
    (AB / "offline/replay-results.json").write_text(json.dumps(results, indent=1))
    m1 = sum(results[f"{r}/k1"]["match"] for r in BASELINE)
    print(f"O2 k=1 decision match: {m1}/6")
    for r in sorted(BASELINE):
        a, b = results[f"{r}/k1"], results[f"{r}/k2"]
        same = a["decisions"] == b["decisions"]
        allov = all(x[2] == "overlap" for x in b["rows"])
        print(f"{r}: k1 {a['decisions']} baseline {a['baseline']} match={a['match']} | k2 same-as-k1={same} all-overlap={allov} | rows k1={a['rows']}")
        for e in a["log"]:
            print("    ", {x: e[x] for x in ("round", "verdict", "decision", "brief_ids", "new", "refound", "regressed", "cleared") if x in e}, e.get("revise"), e["warnings"])


main()
