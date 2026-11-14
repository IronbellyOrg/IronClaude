9166c23cce094921f5b1d325c7ebb588998125b4
Review one task for spec compliance.

Task brief: T5 (source: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/DESIGN.md; task grouping in .dev/implement/collab-r1-move-radar/tasks.md). Covers DESIGN.md section 1.2 rows `tools/collab_summary.py` (pre and post; its `catcheck` subcommand was reviewed under T1), `tools/anon.sh`, `tools/results.py`, `tools/alarms.py`, `tools/cleanup-sessions.sh`, the behaviour of sections 2.8 (contamination safeguards: the post-run checks), 2.9 (metrics, collab.json, alarms), 2.10 (the detections implemented in collab_summary.py / alarms.py), 5.3 (anonymiser and the unchanged judge's path trick) and 5.4 (results row), and the tests T-14, T-15, T-16, T-17, T-18, T-19, F-1, F-2, F-3, F-4 (summary part: pre exits 3 and writes QUARANTINED; launch.sh marking the package and skipping merge/judge is a later task) and the slo_breach part of F-8. F-11 and F-12 (merge refusal, judge retry) need launch.sh and belong to the next task. Implementation notes: launch.sh (next task) writes runs/<row>/<pkg>/run.json (fields used here: collab, role, model, k, T0_MS, FINISH_MS, HANG_MS, B, values, cand_sha256) and runs/<row>/<pkg>/status; the stub `claude` gained a `judge` mode for T-15.
T5.AC1: the five tools implement the behaviour of DESIGN.md sections 2.8, 2.9, 2.10 (summary and alarm detections), 5.3 and 5.4.
T5.AC2: T-14, T-15, T-16, T-17, T-18, T-19, F-1, F-2, F-3, F-4 (summary part) and F-8 (slo_breach part) exist as tests that check what DESIGN.md 6.1/6.2 lists for them and pass: `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests -q`.
Global constraints: Orchestrator constraints: Create and edit files ONLY under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/ (plus .dev/implement/collab-r1-move-radar/ and scratch under /tmp/evalsb-collab-r1/ and /tmp/collab-r1/). Do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder, or any other redesign's folder. Do not stage, commit or push. Use uv for all Python. Gateway model sessions only under flock /tmp/collab-gateway.lock; models muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7; Opus only as blind judge; never Qwen or glm; NOFALLBACK=1. No full panel runs. Design hard limits: DESIGN.md section 0 'Hard limits carried into every script'.
Start sha: 9166c23cce094921f5b1d325c7ebb588998125b4
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/collab_summary.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/collab_summary.py
deleted file mode 100644
index fd7eefb69..000000000
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/collab_summary.py
+++ /dev/null
@@ -1,60 +0,0 @@
-"""collab_summary.py: audits, quarantine and collab.json for one package of one row (R-23, R-09).
-
-Usage (run from REPO with `uv run python`):
-  collab_summary.py pre  <row> <pkg> [--root <R1>] [--sb <SB>]
-  collab_summary.py post <row> <pkg> [--root <R1>] [--sb <SB>]
-  collab_summary.py catcheck <catalogue.json> <ground-truth.json>...   (G-PINS, R-07)
-"""
-
-from __future__ import annotations
-
-import json
-import sys
-
-WINDOW = 12
-
-
-def gt_hits(texts: list[str], quotes: list[str]) -> list[dict]:
-    """Every 12-character window of a ground-truth plan_quote found inside one of the texts."""
-    flat = lambda s: " ".join(s.split())  # noqa: E731
-    hits = []
-    for qi, q in enumerate(quotes):
-        q = flat(q)
-        wins = {q[i : i + WINDOW] for i in range(max(0, len(q) - WINDOW + 1))}
-        for ti, t in enumerate(texts):
-            t = flat(t)
-            for w in sorted(wins):
-                if w in t:
-                    hits.append({"quote": qi, "text": ti, "window": w})
-                    break
-    return hits
-
-
-def catalogue_texts(cat: dict) -> list[str]:
-    out = []
-    for m, t in cat["moves"].items():
-        out.append(t)
-        if m in cat["observable"]:
-            out.append(t + cat["observable_suffix"])
-    return out + [cat["src_text"], cat["finish_text"]]
-
-
-def gt_quotes(paths: list[str]) -> list[str]:
-    return [it["plan_quote"] for p in paths for it in json.load(open(p))["items"] if it.get("plan_quote")]
-
-
-def cmd_catcheck(cat_path: str, gt_paths: list[str]) -> int:
-    hits = gt_hits(catalogue_texts(json.load(open(cat_path))), gt_quotes(gt_paths))
-    print(json.dumps({"ground_truth_files": len(gt_paths), "hits": hits, "pass": not hits}))
-    return 0 if not hits else 1
-
-
-def main(argv: list[str]) -> int:
-    if len(argv) >= 3 and argv[0] == "catcheck":
-        return cmd_catcheck(argv[1], argv[2:])
-    print(__doc__, file=sys.stderr)
-    return 2
-
-
-if __name__ == "__main__":
-    sys.exit(main(sys.argv[1:]))
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/collab_summary.py
index 000000000..7c6a039e2 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/collab_summary.py
@@ -1,19 +1,36 @@
-"""collab_summary.py: audits, quarantine and collab.json for one package of one row (R-23, R-09).
+"""collab_summary.py: audits, quarantine and collab.json for one package of one row (R-23, R-09, R-25 inputs).
 
 Usage (run from REPO with `uv run python`):
-  collab_summary.py pre  <row> <pkg> [--root <R1>] [--sb <SB>]
-  collab_summary.py post <row> <pkg> [--root <R1>] [--sb <SB>]
-  collab_summary.py catcheck <catalogue.json> <ground-truth.json>...   (G-PINS, R-07)
+  collab_summary.py pre  <row> <pkg> [--root R1] [--sb SB] [--a1 A1DIR]   after the reviewers, before the merge
+  collab_summary.py post <row> <pkg> [--root R1] [--sb SB] [--a1 A1DIR]   after the anonymiser: ledger_rows, anon_leak
+  collab_summary.py catcheck <catalogue.json> <ground-truth.json>...       (G-PINS, R-07)
+pre exits 3 and writes runs/<row>/<pkg>/QUARANTINED on a hard audit failure (DESIGN.md sections 2.2, 2.8, 2.9, 2.10).
 """
 
 from __future__ import annotations
 
+import glob
+import itertools
 import json
+import os
+import re
+import subprocess
 import sys
 
+from superclaude.cli.review import findings as fnd
+
+REPO = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel"
+TOOLS = os.path.dirname(os.path.abspath(__file__))
+R1 = os.path.dirname(TOOLS)
+A1DIR = f"{REPO}/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
+SB = "/tmp/evalsb-collab-r1"
 WINDOW = 12
+SEARCH_MOVES = ["M1", "M2", "M4", "M7"]
+NULL_REVIEWER = {"resume_fallback": None, "phase2_s": None, "phase2_timeout": None, "p2_lines_salvaged": None,
+                 "n_planned": None, "n_launched": None, "stop_blocks": 0, "over_cap": 0, "msgs_sent": 0, "late": 0}
 
 
+# ---------------------------------------------------------------- ground-truth windows (R-07)
 def gt_hits(texts: list[str], quotes: list[str]) -> list[dict]:
     """Every 12-character window of a ground-truth plan_quote found inside one of the texts."""
     flat = lambda s: " ".join(s.split())  # noqa: E731
@@ -49,9 +66,315 @@ def cmd_catcheck(cat_path: str, gt_paths: list[str]) -> int:
     return 0 if not hits else 1
 
 
+# ---------------------------------------------------------------- helpers
+def jsonl(path: str) -> list[dict]:
+    """Objects of a JSONL file; torn, corrupt or non-object lines are skipped (R-22)."""
+    out = []
+    try:
+        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
+    except OSError:
+        return out
+    for ln in lines:
+        try:
+            v = json.loads(ln)
+        except ValueError:
+            continue
+        if isinstance(v, dict):
+            out.append(v)
+    return out
+
+
+def load(path: str, default=None):
+    try:
+        return json.load(open(path))
+    except (OSError, ValueError):
+        return default
+
+
+def p95(xs: list[float]):
+    if not xs:
+        return None
+    s = sorted(xs)
+    return s[max(0, -(-95 * len(s) // 100) - 1)]
+
+
+def classify(records: list[dict], index_path: str, srcpath: str) -> list[dict]:
+    """Run radar-classify.jq over tele records -> [{"n","sig"}] in the same order."""
+    if not records:
+        return []
+    r = subprocess.run(["jq", "-c", "--slurpfile", "ix", index_path, "--arg", "srcpath", srcpath, "-f", f"{TOOLS}/radar-classify.jq"],
+                       input="\n".join(json.dumps(x) for x in records) + "\n", capture_output=True, text=True, check=True)
+    return [json.loads(x) for x in r.stdout.splitlines()]
+
+
+def transcript_records(review_dir: str, rid: str) -> list[dict]:
+    """Tele-shaped records from the --output-format json transcripts (collab 0 has no hook telemetry)."""
+    out, n = [], 0
+    for att in sorted(glob.glob(f"{review_dir}/{rid}.attempt*.json")):
+        entries = load(att, [])
+        for en in entries if isinstance(entries, list) else []:
+            if not isinstance(en, dict) or en.get("type") != "assistant":
+                continue
+            sub = bool(en.get("parent_tool_use_id"))
+            for c in (en.get("message") or {}).get("content") or []:
+                if isinstance(c, dict) and c.get("type") == "tool_use":
+                    if not sub:
+                        n += 1
+                    out.append({"n": None if sub else n, "t": None, "rid": rid, "sub": sub, "tool": c.get("name"), "input": c.get("input") or {}})
+    return out
+
+
+def task_sections(cand: str) -> list[tuple[int, int, str]]:
+    """(start line, end line, Task id) for each '## Task N:' section, 0-based half-open."""
+    lines = cand.splitlines()
+    heads = [(i, "T" + re.match(r"^## Task (\d+):", ln).group(1)) for i, ln in enumerate(lines) if re.match(r"^## Task \d+:", ln)]
+    out = []
+    for i, t in heads:
+        end = len(lines)
+        for k in range(i + 1, len(lines)):
+            if lines[k].startswith("## "):
+                end = k
+                break
+        out.append((i, end, t))
+    return out
+
+
+def tasks_of_report(report: str, cand: str, sections) -> set[str]:
+    """Task ids whose section contains the anchor of a parsed finding (own_line_jaccard input)."""
+    out = set()
+    for f in fnd.parse_block(report)["findings"]:
+        for a, _b in fnd.locate(cand, f["anchor"]):
+            for s, e, t in sections:
+                if s <= a < e:
+                    out.add(t)
+    return out
+
+
+def mean_pairwise_jaccard(sets: list[set]):
+    pairs = list(itertools.combinations(sets, 2))
+    if not pairs:
+        return None
+    js = [len(a & b) / len(a | b) if (a | b) else 0.0 for a, b in pairs]  # an empty pair counts 0
+    return sum(js) / len(js)
+
+
+def validate_pairs(pairs: list[dict], cat_path: str, searcher: str, readers: list[str]) -> list[dict]:
+    r = subprocess.run(["bash", f"{TOOLS}/msg-validate.sh", cat_path, searcher, ",".join(readers)],
+                       input="".join(json.dumps(p) + "\n" for p in pairs), capture_output=True, text=True)
+    return [json.loads(x) for x in r.stderr.splitlines() if x.startswith("{")]
+
+
+# ---------------------------------------------------------------- pre / post
+def pre(row: str, pkg: str, root: str, sb: str, a1: str) -> int:
+    d = f"{root}/runs/{row}/{pkg}"
+    rev, board = f"{d}/reviews", f"{d}/board"
+    run = load(f"{d}/run.json")
+    collab = int(run["collab"])
+    roles = run["role"]
+    rids = list(roles)
+    searcher = next(r for r in rids if roles[r] == "searcher")
+    readers = [r for r in rids if roles[r] == "reader"]
+    cat_path = f"{board}/ctx/catalogue.json" if os.path.exists(f"{board}/ctx/catalogue.json") else f"{root}/config/catalogue.json"
+    index_path = f"{root}/index/{pkg}.json"  # post hoc uses the index on disk, not the board's frozen copy (F-1)
+    srcpath = f"{sb}/cand/{pkg}/source.md"
+    hard, flags = [], []
+    metas = {r: load(f"{rev}/{r}.meta.json", {}) for r in rids}
+
+    # telemetry: hook tele (collab 1) or transcript tool_use blocks (collab 0, post-hoc coverage counters)
+    tele = {r: jsonl(f"{board}/tele/{r}.jsonl") if collab else transcript_records(rev, r) for r in rids}
+    metrics = {r: jsonl(f"{board}/metrics/{r}.jsonl") for r in rids}
+    allrec = [x for r in rids for x in tele[r]]
+    sig_of = classify(allrec, index_path, srcpath)
+    sigs, i = {r: [] for r in rids}, 0
+    for r in rids:
+        for rec in tele[r]:
+            sigs[r].append((rec, set(sig_of[i]["sig"])))
+            i += 1
+
+    # board lines and inject events pair one to one; every pair passes the validator (leak lookup, section 2.2)
+    mpath = f"{board}/msgs/radar.jsonl"
+    raw_msgs = open(mpath).read().splitlines() if os.path.exists(mpath) else []
+    injects = {e["id"]: (r, e) for r in rids for e in metrics[r] if e.get("ev") == "inject"}
+    by_id = {}
+    for raw in raw_msgs:
+        try:
+            by_id[json.loads(raw).get("id")] = raw
+        except (ValueError, AttributeError):
+            hard.append(f"board line not a JSON object: {raw[:80]}")
+    pairs = []
+    for mid, raw in by_id.items():
+        if mid not in injects:
+            hard.append(f"board line {mid} has no inject event")
+        else:
+            pairs.append({"line": raw, "text": injects[mid][1].get("text")})
+    for mid in injects:
+        if mid not in by_id:
+            hard.append(f"inject event {mid} has no board line")
+    rejects = validate_pairs(pairs, cat_path, searcher, readers) if pairs else []
+    hard += [f"validator {x['reject']}" for x in rejects]
+    if any('"task_hint"' in raw for raw in raw_msgs):
+        hard.append("task_hint in a board line")
+
+    # ground truth and read-only audits (R-09, Redesign 1 (e), section 2.8)
+    gt = f"{a1}/{pkg}/ground-truth.json"
+    quotes = gt_quotes([gt]) if os.path.exists(gt) else []
+    gth = gt_hits(raw_msgs, quotes)
+    if gth:
+        hard.append(f"{len(gth)} board line(s) hold a 12-character ground-truth window")
+    gt_tele = [r for r in rids for rec in tele[r] if re.search(r"\.dev/reflect|ground-truth", json.dumps(rec.get("input")))]
+    if gt_tele:
+        hard.append(f"tele names .dev/reflect or ground-truth ({len(gt_tele)} record(s))")
+    repo = f"{sb}/{pkg}/repo"
+    st = subprocess.run(["git", "-C", repo, "status", "--porcelain"], capture_output=True, text=True)
+    dirty = st.returncode != 0 or bool(st.stdout.strip())
+    if dirty:
+        hard.append("sandbox git status not clean")
+    if os.path.exists(f"{repo}/.dev/reflect"):
+        hard.append("sandbox holds .dev/reflect")
+    cs = subprocess.run(["sha256sum", f"{sb}/cand/{pkg}/candidate.md"], capture_output=True, text=True).stdout.split()
+    cand_ok = bool(cs) and cs[0] == run.get("cand_sha256")
+    if not cand_ok:
+        hard.append("candidate sha256 changed")
+
+    # live-vs-post-hoc spot check (F-1): an observable move injected although the panel had already done it,
+    # or a no_gap skip although a search move was still uncovered
+    spot = []
+
+    def seen(rr, rec, r, e):  # what the hook could see at that checkpoint: own calls up to n, peers' calls before t
+        if rec.get("sub"):
+            return False
+        if rr == r:
+            return (rec.get("n") or 0) <= (e.get("n") or 0)
+        return (rec.get("t") or 0) < (e.get("t") or 0)
+
+    for mid, (r, e) in injects.items():
+        if e.get("slot_type") != "search":
+            continue
+        done = sorted({rr for rr in rids for rec, s in sigs[rr] if e["move"] in s and seen(rr, rec, r, e)})
+        if done:
+            spot.append({"id": mid, "move": e["move"], "live": "uncovered", "post_hoc": "covered", "by": done})
+    for r in rids:
+        for e in metrics[r]:
+            if e.get("ev") == "skip" and e.get("reason") == "no_gap" and roles[r] == "searcher":
+                # the skip event carries n only (section 2.4); its time is that of the own tele record with that n
+                t = next((rec.get("t") for rec, _ in sigs[r] if rec.get("n") == e.get("n") and not rec.get("sub")), None)
+                e = dict(e, t=e.get("t", t))
+                cov = {m for rr in rids for rec, s in sigs[rr] if seen(rr, rec, r, e) for m in s}
+                miss = [m for m in SEARCH_MOVES if m not in cov]
+                if miss:
+                    spot.append({"n": e.get("n"), "rid": r, "live": "no_gap", "post_hoc_uncovered": miss})
+
+    # per reviewer and per slot
+    finish_ms = run["FINISH_MS"]
+    reviewers, slots = {}, []
+    for r in rids:
+        m, met = metas[r], metrics[r]
+        inj = [e for e in met if e.get("ev") == "inject"]
+        seal = [e for e in met if e.get("ev") == "seal"]
+        fin = [e for e in met if e.get("ev") == "finish"]
+        hook_calls = sum(1 for x in tele[r] if not x.get("sub")) if collab else 0
+        would = (m.get("end_ms") or 0) > finish_ms if not collab else None
+        if not collab:  # the collab-0 board holds only this metrics line (written here, not by a hook)
+            os.makedirs(f"{board}/metrics", exist_ok=True)
+            with open(f"{board}/metrics/{r}.jsonl", "w") as f:
+                f.write(json.dumps({"ev": "finish_would_fire", "value": would}) + "\n")
+        reviewers[r] = dict(NULL_REVIEWER, **{
+            "model": run["model"][r], "role": roles[r], "valid": m.get("valid"), "session_ids": m.get("session_ids", []),
+            "msgs_received": len(inj), "first_delivery_t": inj[0]["t"] if inj else None, "seal_t": seal[0]["t"] if seal else None,
+            "hook_calls": hook_calls, "hook_error": sum(1 for e in met if e.get("ev") == "hook_error"),
+            "hook_ms_p95": p95([e["ms"] for e in met if e.get("ev") == "t" and isinstance(e.get("ms"), (int, float))]),
+            "reask_s": m.get("reask_s"), "attempts": m.get("attempts"), "retry_s": m.get("retry_s"), "retry_isolated": m.get("retry_isolated"),
+            "dropped_lines": m.get("dropped_lines"), "k": run["k"][roles[r]] if collab else 0, "panel_finish_at": finish_ms,
+            "finish_signal_t": fin[0]["t"] if fin else None, "finish_would_fire": would, "hang_kill": m.get("hang_kill"),
+            "snapshot_missing": sum(1 for e in met if e.get("ev") == "snapshot_missing"),
+            "isolated": bool(collab) and (hook_calls == 0 or bool(m.get("retry_isolated"))),
+            "start_ms": m.get("start_ms"), "end_ms": m.get("end_ms")})
+        for e in inj:
+            ex = None
+            if e.get("slot_type") == "search" and e.get("move"):
+                ex = any(e["move"] in s for rec, s in sigs[r] if not rec.get("sub") and (rec.get("n") or 0) > e["n"])
+            slots.append({"rid": r, "id": e["id"], "n": e["n"], "t": e["t"], "slot_type": e.get("slot_type"), "move": e.get("move"),
+                          "task_hint": e.get("task_hint", []), "move_executed": ex, "card_form": None, "deal_r": None, "deal_c": None})
+        if collab and hook_calls == 0:
+            flags.append(f"ALARM hook_calls=0 {r}")
+
+    # panel
+    ends = [m.get("end_ms") for m in metas.values() if m.get("end_ms")]
+    elapsed = (max(ends) - run["T0_MS"]) / 1000 if ends else None
+    B = run["B"]  # noqa: N806 (the design's symbol)
+    cand = open(f"{sb}/cand/{pkg}/candidate.md").read()
+    secs = task_sections(cand)
+    tsets = []
+    for r in rids:
+        try:
+            tsets.append(tasks_of_report(open(f"{rev}/{r}.md").read(), cand, secs))
+        except OSError:
+            tsets.append(set())
+    jac = mean_pairwise_jaccard(tsets)
+    cover = {s: sum(1 for r in rids for rec, ss in sigs[r] if not rec.get("sub") and s in ss)
+             for s in ["M1", "M2", "M4", "M7", "SRC_OPENED", "UNNAMED_TEST"]}
+    byk: dict[str, int] = {}
+    for s in slots:
+        byk[s["move"] or "SRC"] = byk.get(s["move"] or "SRC", 0) + 1
+    hang_s = (run["HANG_MS"] - run["T0_MS"]) / 1000
+    collab_json = {
+        "schema": "r1-collab/1", "row": row, "pkg": pkg, "arm": "A6-F3" if collab else "A1", "collab": collab,
+        "panel_finish_at": finish_ms, "values_sha256": run.get("values"), "echo_rate": None,
+        "reviewers": reviewers, "slots": slots,
+        "elapsed_s": elapsed, "baseline_elapsed_s": B, "overhead_pct": (100 * (elapsed / B - 1)) if elapsed is not None else None,
+        "own_line_jaccard": jac, "pairwise_task_jaccard": jac, "task_sets": {r: sorted(t) for r, t in zip(rids, tsets)},
+        "ledger_rows": None, "anon_leak": None,
+        "slo_breach": any(bool(m.get("hang_kill")) for m in metas.values()) or (elapsed is not None and elapsed > hang_s),
+        "moves_covered": cover, "injections_by_move": byk, "alarms": flags,
+    }
+    audit = {"schema": "r1-audit/1", "row": row, "pkg": pkg, "hard_failures": hard, "sandbox_clean": not dirty,
+             "candidate_sha_unchanged": cand_ok, "gt_substrings_in_board": len(gth), "tele_naming_ground_truth": len(gt_tele),
+             "validator_rejects": rejects, "spot_check": spot, "leak_violations": len(rejects) + len(gth), "anon_leak": None}
+    json.dump(collab_json, open(f"{d}/collab.json", "w"), indent=1)
+    json.dump(audit, open(f"{d}/audit.json", "w"), indent=1)
+    for a in flags:
+        print(a)
+    if hard:  # quarantine in place, nothing deleted (R-26)
+        with open(f"{d}/QUARANTINED", "w") as f:
+            f.write("; ".join(hard) + "\n")
+        print(f"QUARANTINED {row}/{pkg}: {'; '.join(hard)}", file=sys.stderr)
+        return 3
+    return 0
+
+
+LEAK_PATTERNS = [r"\bc[01]\b", r"\bradar\b", r"evalsb-collab-r1", r"\bt[0-9a-z]+-[0-9]+\b"]
+
+
+def post(row: str, pkg: str, root: str, sb: str, a1: str) -> int:
+    d = f"{root}/runs/{row}/{pkg}"
+    c, a = load(f"{d}/collab.json"), load(f"{d}/audit.json")
+    led = load(f"{d}/ledger.json")
+    c["ledger_rows"] = len(led["rows"]) if led else None
+    key = load(f"{d}/label-key.json")
+    leak = None
+    if key:
+        p = f"{root}/scoring/{key['opaque']}/{pkg}/{key['label']}/merged-anon.md"
+        if os.path.exists(p):
+            text = open(p).read()
+            leak = text.count(row) + sum(len(re.findall(x, text)) for x in LEAK_PATTERNS)
+    c["anon_leak"] = a["anon_leak"] = leak
+    json.dump(c, open(f"{d}/collab.json", "w"), indent=1)
+    json.dump(a, open(f"{d}/audit.json", "w"), indent=1)
+    return 0
+
+
 def main(argv: list[str]) -> int:
     if len(argv) >= 3 and argv[0] == "catcheck":
         return cmd_catcheck(argv[1], argv[2:])
+    opts = {"--root": R1, "--sb": SB, "--a1": A1DIR}
+    rest, it = [], iter(argv)
+    for x in it:
+        if x in opts:
+            opts[x] = next(it)
+        else:
+            rest.append(x)
+    if len(rest) == 3 and rest[0] in ("pre", "post"):
+        return (pre if rest[0] == "pre" else post)(rest[1], rest[2], opts["--root"], opts["--sb"], opts["--a1"])
     print(__doc__, file=sys.stderr)
     return 2
 
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/anon.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/anon.sh
new file mode 100755
index 000000000..532d6ce8f
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/anon.sh
@@ -0,0 +1,37 @@
+#!/usr/bin/env bash
+# anon.sh <row> <pkg> [--root R1]   (DESIGN.md section 5.3, adapted from A1DIR/tools/tmp-scripts/anon-b11.sh)
+# runs/<row>/<pkg>/merged-1.md -> scoring/<opaque>/<pkg>/<L>/merged-anon.md; key runs/<row>/<pkg>/label-key.json
+# = {"opaque","label"} (never under scoring/). A re-run reuses the recorded key. Prints the scoring path.
+set -u -o pipefail
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+R1REAL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
+A1DIR=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
+SB=/tmp/evalsb-collab-r1
+ROW=${1:?usage: anon.sh <row> <pkg> [--root R1]}; PKG=${2:?}; shift 2
+R1=$R1REAL
+while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
+D=$R1/runs/$ROW/$PKG; SRC=$D/merged-1.md; KEY=$D/label-key.json
+[ -f "$SRC" ] || { echo "FAIL no $SRC" >&2; exit 1; }
+if [ -f "$KEY" ]; then
+  OP=$(jq -r .opaque "$KEY"); L=$(jq -r .label "$KEY")
+else
+  OP=$(od -An -N6 -tx1 /dev/urandom | tr -d ' \n')
+  L=$(printf 'Q\nR\nS\nT\nU\nV\n' | shuf -n1)
+  jq -n -c --arg o "$OP" --arg l "$L" '{opaque:$o,label:$l}' > "$KEY"
+fi
+OUT=$R1/scoring/$OP/$PKG/$L; mkdir -p "$OUT"
+esc() { printf '%s' "$1" | sed 's/[][\.*^$|]/\\&/g'; }
+# 1. absolute R1 (the real one and a test root) and A1DIR -> <EVAL>; the sandbox root -> /tmp/evalsb
+sed -e "s|$(esc "$R1")|<EVAL>|g" -e "s|$(esc "$R1REAL")|<EVAL>|g" -e "s|$(esc "$A1DIR")|<EVAL>|g" -e "s|$(esc "$SB")|/tmp/evalsb|g" \
+  "$SRC" > "$OUT/merged-anon.md.tmp"
+# 2. reviewer ids -> R1, R2, R3 in sorted order
+i=1
+for ID in $(grep -oE '\bt[0-9a-z]+-[0-9]+\b' "$OUT/merged-anon.md.tmp" | sort -u); do
+  sed -i "s/\b$ID\b/R$i/g" "$OUT/merged-anon.md.tmp"; i=$((i + 1))
+done
+# 3. the two rules of anon-b11.sh:24-25, then drop any "origin" key (defensive; F3 never writes one)
+sed -i -e 's|^candidate: <EVAL>/[^ ]*/candidate.md sha256|candidate: <candidate file> sha256|' \
+       -e 's|report <EVAL>/[^ ,]*|report <redacted>|g' \
+       -e 's/,\s*"origin"\s*:\s*"[^"]*"//g' -e 's/"origin"\s*:\s*"[^"]*"\s*,\s*//g' "$OUT/merged-anon.md.tmp"
+mv "$OUT/merged-anon.md.tmp" "$OUT/merged-anon.md"
+echo "$OUT"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/results.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/results.py
new file mode 100644
index 000000000..895935d62
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/results.py
@@ -0,0 +1,162 @@
+"""results.py: the results row of one launch (DESIGN.md section 5.4, schema r1-results/1).
+
+Usage (from REPO): uv run python tools/results.py <row> [--root R1] [--a1 A1DIR]
+Reads runs/<row>/<pkg>/{status,run.json,collab.json,audit.json,label-key.json,reviews/*.cost.json,reviews/*.meta.json},
+the judge's scoring/<opaque>/<pkg>/<L>/score.json and A1DIR/<pkg>/ground-truth.json (id and blocking_in_implement only).
+Writes results/<row>.json and appends one line to results/results.jsonl; refuses (exit 2) a row id already there.
+Definitions as A1DIR/analysis/final-table.py:31-37: any = |gt_covered_any|, jb = |gt_covered_blocking|,
+rb = judge-blocking items whose blocking_in_implement is true, wb = wrong_blockers.
+"""
+
+from __future__ import annotations
+
+import glob
+import json
+import os
+import re
+import sys
+
+REPO = "/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel"
+R1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
+A1DIR = f"{REPO}/.dev/eval-workspaces/tasklist-review-panel/20261111-a1"
+DS, AL, DE = "TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"
+PKGS = [DS, AL, DE]
+
+
+def load(p, default=None):
+    try:
+        return json.load(open(p))
+    except (OSError, ValueError):
+        return default
+
+
+def package(root: str, a1: str, row: str, pkg: str) -> tuple[dict, dict | None]:
+    d = f"{root}/runs/{row}/{pkg}"
+    if not os.path.isdir(d):
+        return {"status": "not_run"}, None
+    status = open(f"{d}/status").read().strip() if os.path.exists(f"{d}/status") else "invalid"
+    c = load(f"{d}/collab.json", {}) or {}
+    run = load(f"{d}/run.json", {}) or {}
+    key = load(f"{d}/label-key.json")
+    score = load(f"{root}/scoring/{key['opaque']}/{pkg}/{key['label']}/score.json") if key else None
+    if status == "ok" and score is None:
+        status = "judge_failed"
+    costs = [load(f, {}) for f in glob.glob(f"{d}/reviews/*.cost.json")]
+    metas = [load(f, {}) for f in glob.glob(f"{d}/reviews/*.meta.json") if ".attempt" not in f]
+    out = {"status": status, "label": key["label"] if key else None,
+           "ledger_rows": c.get("ledger_rows"), "output_tokens": sum(x.get("total_output_tokens_all", 0) for x in costs),
+           "elapsed_s": c.get("elapsed_s"), "B_f": c.get("baseline_elapsed_s"), "overhead_pct": c.get("overhead_pct"),
+           "slo_breach": c.get("slo_breach"), "k": run.get("k"), "values": run.get("values"),
+           "dropped_lines": sum(m.get("dropped_lines") or 0 for m in metas),
+           "reask": sum(1 for m in metas if m.get("reask_s") is not None),
+           "retry_isolated": sum(1 for m in metas if m.get("retry_isolated")),
+           "hang_kill": sum(1 for m in metas if m.get("hang_kill")),
+           "gt_covered_any": None, "real_blocking": None, "judge_blocking": None, "wrong_blockers": None}
+    if status == "ok":
+        gt = {i["id"]: i["blocking_in_implement"] for i in load(f"{a1}/{pkg}/ground-truth.json")["items"]}
+        out.update({"gt_covered_any": score["gt_covered_any"], "judge_blocking": score["gt_covered_blocking"],
+                    "real_blocking": [g for g in score["gt_covered_blocking"] if gt.get(g)], "wrong_blockers": score["wrong_blockers"]})
+    return out, c
+
+
+def build(row: str, root: str, a1: str) -> dict:
+    m = re.fullmatch(r"(el2|sl2|hl2)-c([01])-r(\d+)", row)
+    if not m:
+        raise SystemExit(f"bad row id {row}")
+    panel, collab, rep = m.group(1), int(m.group(2)), int(m.group(3))
+    cfg = json.load(open(f"{root}/config/panels.json"))[panel]["roles"]
+    models = {cfg["searcher"]["rid"]: cfg["searcher"]["model"], **{r: cfg["reader"]["model"] for r in cfg["reader"]["rids"]}}
+    rowrun = load(f"{root}/runs/{row}/run.json", {}) or {}
+    pk, cj = {}, {}
+    for p in PKGS:
+        pk[p], cj[p] = package(root, a1, row, p)
+    ok = {p: pk[p]["status"] == "ok" for p in PKGS}
+
+    def total(ps, f):
+        return sum(f(pk[p]) for p in ps) if all(ok[p] for p in ps) else None
+
+    cnt = {"injections": 0, "injections_by_move": {}, "src_checks": 0, "search_injections": 0, "static_injections": 0,
+           "observable_moves_executed": 0, "skips_no_gap": 0, "skips_guard": 0, "finish_signals": 0, "finish_would_fire": 0,
+           "hook_calls": 0, "hook_errors": 0, "hook_ms_p95": None, "snapshot_missing": 0, "late": 0, "receivers": 0,
+           "leak_violations": 0, "moves_covered_panel": {}, "own_line_jaccard": {}}
+    for p in PKGS:
+        c = cj[p]
+        if not c:
+            continue
+        a = load(f"{root}/runs/{row}/{p}/audit.json", {}) or {}
+        cnt["leak_violations"] += a.get("leak_violations", 0)
+        for s in c.get("slots", []):
+            cnt["injections"] += 1
+            cnt[{"src": "src_checks", "search": "search_injections", "static": "static_injections"}[s["slot_type"]]] += 1
+            if s["move"]:
+                cnt["injections_by_move"][s["move"]] = cnt["injections_by_move"].get(s["move"], 0) + 1
+            cnt["observable_moves_executed"] += 1 if s.get("move_executed") is True else 0
+        for r, rv in c.get("reviewers", {}).items():
+            met = []
+            mp = f"{root}/runs/{row}/{p}/board/metrics/{r}.jsonl"
+            for ln in open(mp).read().splitlines() if os.path.exists(mp) else []:
+                try:
+                    v = json.loads(ln)
+                except ValueError:
+                    continue
+                if isinstance(v, dict):
+                    met.append(v)
+            cnt["skips_no_gap"] += sum(1 for e in met if e.get("ev") == "skip" and e.get("reason") == "no_gap")
+            cnt["skips_guard"] += sum(1 for e in met if e.get("ev") == "skip" and e.get("reason") == "guard")
+            cnt["finish_signals"] += 1 if rv.get("finish_signal_t") else 0
+            cnt["finish_would_fire"] += 1 if rv.get("finish_would_fire") else 0
+            cnt["hook_calls"] += rv.get("hook_calls") or 0
+            cnt["hook_errors"] += rv.get("hook_error") or 0
+            cnt["snapshot_missing"] += rv.get("snapshot_missing") or 0
+            cnt["late"] += rv.get("late") or 0
+            cnt["receivers"] += 1 if (rv.get("k") or 0) > 0 else 0
+            if rv.get("hook_ms_p95") is not None:  # the one counter not summed: the worst package p95
+                cnt["hook_ms_p95"] = max(cnt["hook_ms_p95"] or 0, rv["hook_ms_p95"])
+        for s, n in (c.get("moves_covered") or {}).items():
+            cnt["moves_covered_panel"][s] = cnt["moves_covered_panel"].get(s, 0) + n
+        cnt["own_line_jaccard"][p] = c.get("own_line_jaccard")
+    return {
+        "schema": "r1-results/1", "design": "r1-move-radar", "row": row, "panel": panel, "models": models,
+        "collab": collab, "rep": rep, "started_utc": rowrun.get("started_utc"), "values": {p: pk[p].get("values") for p in PKGS},
+        "status": "complete" if all(ok.values()) else "incomplete",
+        "found_14": total([DS, AL], lambda x: len(x["gt_covered_any"])),
+        "real_blocking_8": total([DS, AL], lambda x: len(x["real_blocking"])),
+        "judge_blocking": total([DS, AL], lambda x: len(x["judge_blocking"])),
+        "wrong_blockers": total([DS, AL], lambda x: x["wrong_blockers"]),
+        "control_found_2": total([DE], lambda x: len(x["gt_covered_any"])),
+        "control_wrong_blockers": total([DE], lambda x: x["wrong_blockers"]),
+        "output_tokens": total(PKGS, lambda x: x["output_tokens"]),
+        "elapsed_s": {p: pk[p].get("elapsed_s") for p in PKGS},
+        "packages": pk, "collab_counters": cnt,
+    }
+
+
+def main(argv: list[str]) -> int:
+    root, a1, rest, it = R1, A1DIR, [], iter(argv)
+    for x in it:
+        if x == "--root":
+            root = next(it)
+        elif x == "--a1":
+            a1 = next(it)
+        else:
+            rest.append(x)
+    if len(rest) != 1:
+        print(__doc__, file=sys.stderr)
+        return 2
+    row = rest[0]
+    os.makedirs(f"{root}/results", exist_ok=True)
+    jl = f"{root}/results/results.jsonl"
+    seen = {json.loads(x)["row"] for x in open(jl).read().splitlines() if x.strip()} if os.path.exists(jl) else set()
+    if row in seen:
+        print(f"REFUSE row {row} is already in results.jsonl", file=sys.stderr)
+        return 2
+    res = build(row, root, a1)
+    json.dump(res, open(f"{root}/results/{row}.json", "w"), indent=1)
+    with open(jl, "a") as f:
+        f.write(json.dumps(res) + "\n")
+    print(f"{root}/results/{row}.json")
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main(sys.argv[1:]))
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/alarms.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/alarms.py
new file mode 100644
index 000000000..b38e0870e
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/alarms.py
@@ -0,0 +1,106 @@
+"""alarms.py: arm-level alarms and the time verdict over many rows (R-24, R-25, R-45). DESIGN.md section 2.9.
+
+Usage (from REPO): uv run python tools/alarms.py <panel> [--root R1]     read-only; prints one JSON report.
+Rows with rep 0 (smoke) are ignored. A block = the collab-0 and collab-1 rows of one panel with the same rep.
+- CONVERGENCE fires for a collab-1 row when its own_line_jaccard mean exceeds the collab-0 mean + 0.15, or its ledger rows
+  fall more than 20% below the collab-0 mean (pass: at most 2 of 12 rows).
+- SNAPSHOT fires for a collab-1 row when snapshot_missing exceeds 50% of its receiving reviewers.
+- SLO budget: each package with elapsed_s > 1.35 x B_c spends one unit (budget 1 in 12), B_c = the collab-0 median of that
+  package over the panel's rows.
+- baseline_drift per block = median over packages of (collab-0 elapsed / B_f); outside [0.963, 1.10] the block is reported
+  but not used for the time verdict.
+- SAME_GAPS: every collab-1 row injected the same moves (expected for F3; reported, never a failure).
+"""
+
+from __future__ import annotations
+
+import json
+import os
+import statistics
+import sys
+
+R1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
+
+
+def mean(xs):
+    xs = [x for x in xs if x is not None]
+    return sum(xs) / len(xs) if xs else None
+
+
+def row_jaccard(r):
+    return mean(list((r["collab_counters"].get("own_line_jaccard") or {}).values()))
+
+
+def row_ledger(r):
+    v = [p.get("ledger_rows") for p in r["packages"].values() if p.get("status") == "ok"]
+    return sum(v) if v and None not in v else None
+
+
+def report(rows: list[dict]) -> dict:
+    rows = [r for r in rows if r["rep"] >= 1]
+    c0 = [r for r in rows if r["collab"] == 0]
+    c1 = [r for r in rows if r["collab"] == 1]
+    j0, l0 = mean([row_jaccard(r) for r in c0]), mean([row_ledger(r) for r in c0])
+    conv = []
+    for r in c1:
+        j, ledg = row_jaccard(r), row_ledger(r)
+        why = []
+        if j is not None and j0 is not None and j > j0 + 0.15:
+            why.append(f"jaccard {j:.3f} > {j0:.3f} + 0.15")
+        if ledg is not None and l0 is not None and ledg < 0.8 * l0:
+            why.append(f"ledger_rows {ledg} < 0.8 x {l0:.1f}")
+        if why:
+            conv.append({"row": r["row"], "why": why})
+    snap = [r["row"] for r in c1 if r["collab_counters"].get("receivers")
+            and r["collab_counters"]["snapshot_missing"] > 0.5 * r["collab_counters"]["receivers"]]
+    pkgs = sorted({p for r in rows for p in r["packages"]})
+    b_c = {p: statistics.median([r["packages"][p]["elapsed_s"] for r in c0 if r["packages"].get(p, {}).get("elapsed_s") is not None] or [0]) or None
+          for p in pkgs}
+    arms = {}
+    for name, rs in (("collab0", c0), ("collab1", c1)):
+        spent = [(r["row"], p) for r in rs for p in pkgs
+                 if b_c[p] and r["packages"].get(p, {}).get("elapsed_s") is not None and r["packages"][p]["elapsed_s"] > 1.35 * b_c[p]]
+        npk = sum(1 for r in rs for p in pkgs if r["packages"].get(p, {}).get("elapsed_s") is not None)
+        hist = {}
+        for r in rs:
+            for m, n in r["collab_counters"].get("injections_by_move", {}).items():
+                hist[m] = hist.get(m, 0) + n
+        arms[name] = {"rows": len(rs), "slo_spent": spent, "slo_budget": npk / 12, "slo_over_budget": len(spent) > npk / 12,
+                      "median_overhead_pct": {p: statistics.median(v) if (v := [r["packages"][p]["overhead_pct"] for r in rs
+                                              if r["packages"].get(p, {}).get("overhead_pct") is not None]) else None for p in pkgs},
+                      "injections_by_move": hist}
+    blocks = []
+    for r1 in c1:
+        r0 = next((r for r in c0 if r["rep"] == r1["rep"]), None)
+        if not r0:
+            continue
+        ratios = [r0["packages"][p]["elapsed_s"] / r0["packages"][p]["B_f"] for p in pkgs
+                  if r0["packages"].get(p, {}).get("elapsed_s") and r0["packages"][p].get("B_f")]
+        drift = statistics.median(ratios) if ratios else None
+        blocks.append({"rep": r1["rep"], "baseline_drift": drift, "used": drift is not None and 0.963 <= drift <= 1.10})
+    inj = [json.dumps(r["collab_counters"].get("injections_by_move", {}), sort_keys=True) for r in c1]
+    return {"convergence": {"fired": conv, "count": len(conv), "pass": len(conv) <= 2, "collab0_jaccard_mean": j0, "collab0_ledger_mean": l0},
+            "snapshot": {"fired": snap}, "arms": arms, "blocks": blocks,
+            "same_gaps": len(inj) >= 2 and len(set(inj)) == 1}
+
+
+def main(argv: list[str]) -> int:
+    root = R1
+    if "--root" in argv:
+        i = argv.index("--root")
+        root = argv[i + 1]
+        argv = argv[:i] + argv[i + 2:]
+    if len(argv) != 1:
+        print(__doc__, file=sys.stderr)
+        return 2
+    jl = f"{root}/results/results.jsonl"
+    rows = [json.loads(x) for x in open(jl).read().splitlines() if x.strip()] if os.path.exists(jl) else []
+    rep = report([r for r in rows if r["panel"] == argv[0]])
+    print(json.dumps(rep, indent=1))
+    if rep["same_gaps"]:
+        print("SAME_GAPS every collab-1 row injected the same moves (expected for F3; reported, not a failure)", file=sys.stderr)
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main(sys.argv[1:]))
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/cleanup-sessions.sh b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/cleanup-sessions.sh
new file mode 100755
index 000000000..01c95e842
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/cleanup-sessions.sh
@@ -0,0 +1,23 @@
+#!/usr/bin/env bash
+# cleanup-sessions.sh <row> [--root R1] [--sb SB] [--projects DIR]   (R-46, K-7)
+# Deletes only the Claude session files whose ids this row recorded (reviews/<rid>.meta.json session_ids and
+# collab.json reviewers.*.session_ids), from <projects>/<encoded SB/<pkg>/repo>/<id>.jsonl. Never a directory.
+# Writes runs/<row>/cleanup.log (one DELETED or ABSENT line per id).
+set -u -o pipefail
+REPO=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
+R1=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar
+SB=/tmp/evalsb-collab-r1; PROJ=$HOME/.claude/projects
+ROW=${1:?usage: cleanup-sessions.sh <row> [--root R1] [--sb SB] [--projects DIR]}; shift
+while [ $# -gt 0 ]; do case $1 in --root) R1=$2; shift 2;; --sb) SB=$2; shift 2;; --projects) PROJ=$2; shift 2;; *) echo "bad arg $1" >&2; exit 2;; esac; done
+LOG=$R1/runs/$ROW/cleanup.log; : > "$LOG"
+for D in "$R1/runs/$ROW"/*/; do
+  PKG=$(basename "$D"); [ -d "$D/reviews" ] || continue
+  ENC=$(printf '%s' "$SB/$PKG/repo" | sed 's/[^A-Za-z0-9]/-/g')   # Claude's project-dir encoding of the cwd
+  { jq -r '.session_ids[]? // empty' "$D"/reviews/*.meta.json 2>/dev/null
+    jq -r '.reviewers[]?.session_ids[]? // empty' "$D/collab.json" 2>/dev/null; } | sort -u | while IFS= read -r ID; do
+    case $ID in ''|*/*|*..*) continue;; esac   # an id is a bare name, never a path
+    F=$PROJ/$ENC/$ID.jsonl
+    if [ -f "$F" ] && [ ! -L "$F" ]; then rm -f -- "$F" && echo "DELETED $F"; else echo "ABSENT $F"; fi
+  done >> "$LOG"
+done
+cat "$LOG"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/bin/claude b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/bin/claude
deleted file mode 100755
index a0bbf095d..000000000
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/bin/claude
+++ /dev/null
@@ -1,33 +0,0 @@
-#!/usr/bin/env bash
-# Test stub for `claude` (never the gateway). Call k follows line k of $STUB_DIR/plan (the last line repeats):
-#   replay <file>        print <file> with @@MODEL@@ replaced by the --model argument
-#   misroute <file>      print <file> with @@MODEL@@ replaced by "gpt-6.1-sol" (a different model)
-#   sleep <s>            sleep, then print nothing
-#   exit <code>          exit with <code> (127 = binary missing)
-#   hooks <n> <file>     run the --settings PostToolUse command n times (exit status ignored, as Claude does), then replay
-# argv is saved to $STUB_DIR/argv.<k> (one token per line) and stdin to $STUB_DIR/stdin.<k>.
-D=${STUB_DIR:?STUB_DIR not set}
-k=$(( $(cat "$D/count" 2>/dev/null || echo 0) + 1 )); echo "$k" > "$D/count"
-printf '%s\n' "$@" > "$D/argv.$k"; cat > "$D/stdin.$k"
-ARGS=("$@"); MODEL=""; SETTINGS=""
-for ((i = 0; i < ${#ARGS[@]}; i++)); do
-  case ${ARGS[i]} in --model) MODEL=${ARGS[i+1]};; --settings) SETTINGS=${ARGS[i+1]};; esac
-done
-line=$(sed -n "${k}p" "$D/plan"); [ -n "$line" ] || line=$(tail -n 1 "$D/plan")
-read -r mode a b <<< "$line"
-replay() { sed "s/@@MODEL@@/$2/g" "$1"; }
-case $mode in
-  replay) replay "$a" "$MODEL";;
-  misroute) replay "$a" "gpt-6.1-sol";;
-  sleep) sleep "$a";;
-  exit) exit "$a";;
-  hooks)
-    cmd=$(printf '%s' "$SETTINGS" | jq -r '.hooks.PostToolUse[0].hooks[0].command')
-    printf '{"type":"user"}\n' > "$D/transcript.jsonl"
-    for ((j = 1; j <= a; j++)); do
-      printf '{"session_id":"stub","transcript_path":"%s","hook_event_name":"PostToolUse","tool_name":"Bash","tool_input":{"command":"ls %s"},"tool_response":{}}' \
-        "$D/transcript.jsonl" "$j" | bash -c "$cmd" >> "$D/hook-out.$k" 2>/dev/null
-      echo "rc=$?" >> "$D/hook-rc.$k"
-    done
-    replay "$b" "$MODEL";;
-esac
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/bin/claude
old mode 100644
new mode 100755
index 000000000..38a60ed97
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/bin/claude
@@ -5,6 +5,7 @@
 #   sleep <s>            sleep, then print nothing
 #   exit <code>          exit with <code> (127 = binary missing)
 #   hooks <n> <file>     run the --settings PostToolUse command n times (exit status ignored, as Claude does), then replay
+#   judge <file>         copy <file> to the score.json path named in the judge brief on stdin
 # argv is saved to $STUB_DIR/argv.<k> (one token per line) and stdin to $STUB_DIR/stdin.<k>.
 D=${STUB_DIR:?STUB_DIR not set}
 k=$(( $(cat "$D/count" 2>/dev/null || echo 0) + 1 )); echo "$k" > "$D/count"
@@ -30,4 +31,8 @@ case $mode in
       echo "rc=$?" >> "$D/hook-rc.$k"
     done
     replay "$b" "$MODEL";;
+  judge)  # the blind judge: write <a> (a score.json body) to the score.json path named in the brief, then reply
+    p=$(grep -o 'Write JSON to [^ ]*score.json' "$D/stdin.$k" | head -1 | sed 's/^Write JSON to //')
+    [ -n "$p" ] && cp "$a" "$p"
+    printf '[{"type":"result","subtype":"success","result":"score.json written","session_id":"judge"}]\n';;
 esac
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/ground-truth.json b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/ground-truth.json
new file mode 100644
index 000000000..29bf1a257
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/fixtures/ground-truth.json
@@ -0,0 +1,3 @@
+{"items": [
+ {"id": "GT1", "class": "unpassable-ac", "blocking_in_implement": true, "description": "fixture", "plan_quote": "The guard keeps every retry visible to the operator"},
+ {"id": "GT2", "class": "contradiction", "blocking_in_implement": false, "description": "fixture", "plan_quote": "Edit `docs/guide.md` and `CHANGELOG.md`"}]}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
deleted file mode 100644
index 397445d8b..000000000
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
+++ /dev/null
@@ -1,245 +0,0 @@
-"""Shared fixtures for the r1-move-radar tests. Every test writes only under tmp_path."""
-
-from __future__ import annotations
-
-import json
-import os
-import shutil
-import subprocess
-from pathlib import Path
-
-import pytest
-
-R1 = Path(__file__).resolve().parents[1]
-REPO = R1.parents[4]
-A1DIR = REPO / ".dev/eval-workspaces/tasklist-review-panel/20261111-a1"
-FIX = R1 / "tests" / "fixtures"
-TOOLS = R1 / "tools"
-PKG = "TASK-WF-fixture-20261113-000000"
-
-
-def run(args, *, stdin=None, env=None, cwd=None, timeout=60):
-    return subprocess.run(args, input=stdin, capture_output=True, text=True, env=env, cwd=cwd or REPO, timeout=timeout)
-
-
-@pytest.fixture
-def fake_sb(tmp_path):
-    """A sandbox root with one fixture package: SB/<PKG>/repo (root files, src, tests, docs) and SB/cand/<PKG>/."""
-    sb = tmp_path / "sb"
-    repo = sb / PKG / "repo"
-    for rel in ("src/app/core.py", "src/app/scripts/old.sh", "scripts/run.sh", "tests/app/test_core.py",
-                "tests/app/test_other.py", "docs/guide.md", "CHANGELOG.md", "Makefile"):
-        p = repo / rel
-        p.parent.mkdir(parents=True, exist_ok=True)
-        p.write_text("x\n")
-    (repo / "src/app/sub").mkdir()
-    cand = sb / "cand" / PKG
-    cand.mkdir(parents=True)
-    shutil.copy(FIX / "cand" / "candidate.md", cand / "candidate.md")
-    (cand / "source.md").write_text("# source\n")
-    return sb
-
-
-@pytest.fixture
-def root(tmp_path):
-    """A writable R1 output root (index/, runs/, values/ ...) with the real config copied in."""
-    r = tmp_path / "r1"
-    (r / "config").mkdir(parents=True)
-    for f in (R1 / "config").iterdir():
-        shutil.copy(f, r / "config" / f.name)
-    shutil.copy(R1 / "manifest.json", r / "manifest.json")
-    return r
-
-
-def jload(p):
-    return json.loads(Path(p).read_text())
-
-
-@pytest.fixture
-def clean_env():
-    return {k: v for k, v in os.environ.items()}
-
-
-# ---------------------------------------------------------------- hook kit
-SEARCHER, READERS = "t2b-1", ["t4-1", "t3-1"]
-CAT = jload(R1 / "config" / "catalogue.json")
-ORDERS = {"t2b-1": "M2,M7,M4,M1", "t4-1": "M3,M5,M6,M9,M8,M10", "t3-1": "M8,M10,M3,M5,M6,M9",
-          "t1b-1": "M7,M4,M1,M2", "t2-1": "M1,M2,M7,M4"}
-
-
-class Board:
-    """A board under tmp_path with ctx/ files, a clock file and a transcript, driven call by call."""
-
-    def __init__(self, tmp_path, sb="/tmp/sbX"):
-        self.dir = tmp_path / "board"
-        (self.dir / "ctx").mkdir(parents=True)
-        shutil.copy(R1 / "config" / "catalogue.json", self.dir / "ctx" / "catalogue.json")
-        shutil.copy(FIX / "index.json", self.dir / "ctx" / "index.json")
-        self.repo = f"{sb}/{PKG}/repo"
-        self.src = f"{sb}/cand/{PKG}/source.md"
-        (self.dir / "ctx" / "panel.json").write_text(json.dumps({"searcher": SEARCHER, "readers": READERS, "srcpath": self.src}))
-        self.clock = tmp_path / "clock"
-        self.set_clock(1000)
-        self.transcript = tmp_path / "transcript.jsonl"
-        self.transcript.write_text('{"type":"user"}\n{"type":"assistant"}\n')
-
-    def set_clock(self, ms):
-        self.clock.write_text(str(ms))
-
-    def stdin(self, tool="Bash", inp=None, agent_id=None, transcript=None):
-        d = {"session_id": "s1", "transcript_path": str(transcript or self.transcript), "hook_event_name": "PostToolUse",
-             "tool_name": tool, "tool_input": inp if inp is not None else {"command": "ls"}, "tool_response": {}}
-        if agent_id:
-            d["agent_id"] = agent_id
-        return json.dumps(d)
-
-    def args(self, rid, role, k=2, cps=None, finish=10**9, guard=10**9, order=None):
-        cps = cps or ((6, 10) if role == "searcher" else (8, 12))
-        return [str(self.dir), "row-c1-r0/" + PKG, rid, role, "0", str(finish), str(guard), str(k), str(cps[0]),
-                str(cps[1]), order or ORDERS[rid], PKG, str(self.clock)]
-
-    def call(self, rid, role, env=None, raw_stdin=None, **kw):
-        a = self.args(rid, role, **{k: v for k, v in kw.items() if k in ("k", "cps", "finish", "guard", "order")})
-        s = raw_stdin if raw_stdin is not None else self.stdin(**{k: v for k, v in kw.items() if k in ("tool", "inp", "agent_id", "transcript")})
-        r = run(["bash", str(TOOLS / "radar-hook.sh"), *a], stdin=s, env=env)
-        assert r.returncode == 0, r.stderr
-        return r.stdout.strip()
-
-    def metrics(self, rid):
-        p = self.dir / "metrics" / f"{rid}.jsonl"
-        return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
-
-    def metrics_safe(self, rid):
-        """Metrics lines that are JSON objects (a test may plant junk lines)."""
-        p = self.dir / "metrics" / f"{rid}.jsonl"
-        out = []
-        for x in p.read_text().splitlines() if p.exists() else []:
-            try:
-                v = json.loads(x)
-            except ValueError:
-                continue
-            if isinstance(v, dict):
-                out.append(v)
-        return out
-
-    def events(self, rid, ev):
-        return [m for m in self.metrics(rid) if m.get("ev") == ev]
-
-    def tele(self, rid, line):
-        p = self.dir / "tele" / f"{rid}.jsonl"
-        p.parent.mkdir(exist_ok=True)
-        with p.open("a") as f:
-            f.write(line + "\n")
-
-
-def expected_text(move, role):
-    if move is None:
-        return CAT["src_text"]
-    return CAT["moves"][move] + (CAT["observable_suffix"] if role == "searcher" and move in CAT["observable"] else "")
-
-
-def ctx_text(out):
-    d = json.loads(out)
-    assert list(d) == ["hookSpecificOutput"] and d["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
-    assert set(d["hookSpecificOutput"]) == {"hookEventName", "additionalContext"}
-    return d["hookSpecificOutput"]["additionalContext"]
-
-
-@pytest.fixture
-def board(tmp_path):
-    return Board(tmp_path)
-
-
-# ---------------------------------------------------------------- runner kit (stub claude, never the gateway)
-STUB_BIN = FIX / "bin"
-ANCHOR = "Create `src/app/merge_guard.py` and `src/app/scripts/tool.sh`"
-
-
-def finding(**kw):
-    f = {"id": "F1", "severity": "MAJOR", "blocking": True, "category": "contradiction", "anchor": ANCHOR,
-         "refs": [], "claim": "The module and the script disagree."}
-    f.update(kw)
-    return f
-
-
-def report(*findings_, raw_lines=()):
-    body = "\n".join([json.dumps(f) for f in findings_] + list(raw_lines))
-    return f"review: 1 of 3\n\nCovered everything.\n\n## Findings block\n\n```findings-v1\n{body}\n```\n\nverdict: FAIL\n"
-
-
-def json_reply(text, session="sess-1", tokens=100, model="@@MODEL@@"):
-    return json.dumps([
-        {"type": "system", "subtype": "init"},
-        {"type": "assistant", "timestamp": "2026-11-13T10:00:01.000Z", "parent_tool_use_id": None,
-         "message": {"id": "m1", "model": model, "content": [{"type": "text", "text": "ok"}]}},
-        {"type": "result", "subtype": "success", "result": text, "session_id": session,
-         "usage": {"output_tokens": tokens}, "modelUsage": {model: {"outputTokens": tokens}}}])
-
-
-def stream_reply(text, session="sess-1", tokens=50):
-    return "\n".join(json.dumps(x) for x in [
-        {"type": "system", "subtype": "init", "session_id": session},
-        {"type": "assistant", "message": {"id": "m2", "model": "@@MODEL@@", "content": [{"type": "text", "text": text}]}},
-        {"type": "result", "subtype": "success", "result": text, "session_id": session,
-         "modelUsage": {"@@MODEL@@": {"outputTokens": tokens}}}]) + "\n"
-
-
-class Runner:
-    """runs/<row>/<pkg>/ with run.json under a tmp R1 root, a tmp sandbox and a stub plan."""
-
-    def __init__(self, tmp_path, root, hang_s=600, row="el2-c1-r0"):
-        self.root, self.row = root, row
-        self.sb = tmp_path / "sb"
-        (self.sb / PKG / "repo").mkdir(parents=True)
-        (self.sb / "cand" / PKG).mkdir(parents=True)
-        shutil.copy(FIX / "cand" / "candidate.md", self.sb / "cand" / PKG / "candidate.md")
-        (self.sb / "cand" / PKG / "source.md").write_text("# source\n")
-        self.d = root / "runs" / row / PKG
-        (self.d / "settings").mkdir(parents=True)
-        import time
-        t0 = int(time.time() * 1000)
-        self.t0 = t0
-        self.write_run(hang_ms=t0 + int(hang_s * 1000))
-        self.stub = tmp_path / "stub"
-        self.stub.mkdir()
-        self.n = 0
-        self.env = dict(os.environ, PATH=f"{STUB_BIN}:{os.environ['PATH']}", NOFALLBACK="1", STUB_DIR=str(self.stub))
-
-    def write_run(self, hang_ms):
-        (self.d / "run.json").write_text(json.dumps({"T0_MS": self.t0, "HANG_MS": hang_ms, "FINISH_MS": hang_ms, "GUARD_MS": hang_ms,
-                                                     "role": {"t2b-1": "searcher", "t4-1": "reader", "t3-1": "reader"},
-                                                     "T_report": {"searcher": 1, "reader": 1}}))
-
-    def file(self, content):
-        self.n += 1
-        p = self.stub / f"reply{self.n}"
-        p.write_text(content)
-        return p
-
-    def plan(self, *lines):
-        (self.stub / "plan").write_text("\n".join(lines) + "\n")
-
-    def settings(self, rid, board="/nonexistent/board"):
-        r = run(["bash", str(TOOLS / "settings-gen.sh"), board, f"{self.row}/{PKG}", rid, "searcher", "0", "99999999999999", "99999999999999", "2", "6",
-                 "10", "M2,M7,M4,M1", PKG, ""])
-        (self.d / "settings" / f"{rid}.json").write_text(r.stdout)
-        return r.stdout.strip()
-
-    def run(self, rid="t2b-1", model="muse-ember-1.0", collab=1, print_cmd=False, timeout=120):
-        a = ["bash", str(TOOLS / "run-reviewer.sh")] + (["--print-cmd"] if print_cmd else []) + \
-            [self.row, PKG, rid, model, str(collab), str(self.t0), "--root", str(self.root), "--sb", str(self.sb)]
-        return run(a, env=self.env, timeout=timeout)
-
-    def meta(self, rid="t2b-1"):
-        return jload(self.d / "reviews" / f"{rid}.meta.json")
-
-    def argv(self, k):
-        return (self.stub / f"argv.{k}").read_text().splitlines()
-
-    def calls(self):
-        return int((self.stub / "count").read_text()) if (self.stub / "count").exists() else 0
-
-
-@pytest.fixture
-def runner(tmp_path, root):
-    return Runner(tmp_path, root)
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
index 000000000..3a7202edd 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/conftest.py
@@ -243,3 +243,67 @@ class Runner:
 @pytest.fixture
 def runner(tmp_path, root):
     return Runner(tmp_path, root)
+
+
+# ---------------------------------------------------------------- package kit (collab_summary, results, launch tests)
+class Pkg:
+    """runs/<row>/<pkg>/ with run.json, reviews and (collab 1) a live board, a clean git sandbox and a tmp A1DIR."""
+
+    def __init__(self, tmp_path, root, row="el2-c1-r0", collab=1, pkg=PKG):
+        self.root, self.row, self.pkg, self.collab = root, row, pkg, collab
+        self.sb = tmp_path / "sb"
+        repo = self.sb / pkg / "repo"
+        if not repo.exists():
+            (repo / "src").mkdir(parents=True)
+            (repo / "src" / "a.py").write_text("x\n")
+            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
+            subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
+            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "s"], cwd=repo, check=True)
+        cand = self.sb / "cand" / pkg
+        cand.mkdir(parents=True, exist_ok=True)
+        shutil.copy(FIX / "cand" / "candidate.md", cand / "candidate.md")
+        (cand / "source.md").write_text("# source\n")
+        (root / "index").mkdir(exist_ok=True)
+        shutil.copy(FIX / "index.json", root / "index" / f"{pkg}.json")
+        self.a1 = tmp_path / "a1"
+        (self.a1 / pkg).mkdir(parents=True, exist_ok=True)
+        shutil.copy(FIX / "ground-truth.json", self.a1 / pkg / "ground-truth.json")
+        self.d = root / "runs" / row / pkg
+        (self.d / "reviews").mkdir(parents=True, exist_ok=True)
+        import hashlib
+        self.run = {"row": row, "pkg": pkg, "panel": "el2", "collab": collab, "T0_MS": 0, "FINISH_MS": 10**12, "GUARD_MS": 10**12,
+                    "HANG_MS": 174000, "B": 116, "values": "planning", "k": {"searcher": 2, "reader": 2},
+                    "T_report": {"searcher": 3.2, "reader": 6.4}, "role": {"t2b-1": "searcher", "t4-1": "reader", "t3-1": "reader"},
+                    "model": {"t2b-1": "muse-ember-1.0", "t4-1": "gpt-6-luna", "t3-1": "gpt-6-luna"},
+                    "cand_sha256": hashlib.sha256((cand / "candidate.md").read_bytes()).hexdigest()}
+        self.write_run()
+        self.board = Board(self.d, sb=str(self.sb)) if collab else None
+        for rid in self.run["role"]:
+            self.review(rid, report())
+
+    def write_run(self):
+        (self.d / "run.json").write_text(json.dumps(self.run))
+
+    def review(self, rid, text, end_ms=100_000, **meta):
+        (self.d / "reviews" / f"{rid}.md").write_text(text)
+        m = {"reviewer_id": rid, "valid": True, "model_ok": True, "start_ms": 0, "end_ms": end_ms, "attempts": 1,
+             "session_ids": [f"sess-{rid}"], "reask_s": None, "retry_s": None, "retry_isolated": False, "dropped_lines": 0,
+             "hang_kill": False}
+        m.update(meta)
+        (self.d / "reviews" / f"{rid}.meta.json").write_text(json.dumps(m))
+
+    def summary(self, cmd="pre"):
+        return run(["uv", "run", "python", str(TOOLS / "collab_summary.py"), cmd, self.row, self.pkg, "--root", str(self.root),
+                    "--sb", str(self.sb), "--a1", str(self.a1)], cwd=REPO)
+
+    def collab_json(self):
+        return jload(self.d / "collab.json")
+
+    def audit(self):
+        return jload(self.d / "audit.json")
+
+
+@pytest.fixture
+def pkg1(tmp_path, root):
+    return Pkg(tmp_path, root)
+CAND_LONG = (FIX / "cand" / "candidate.md").read_text().split("\n\n")[-1].strip()
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_collab_summary.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_collab_summary.py
new file mode 100644
index 000000000..627484ea1
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_collab_summary.py
@@ -0,0 +1,121 @@
+"""T-17: collab_summary.py pre/post, R-23 keys, Jaccard, move_executed, elapsed and audits."""
+
+import json
+
+import pytest
+from conftest import CAND_LONG, Pkg, finding, report
+
+R23_PANEL = ["arm", "panel_finish_at", "elapsed_s", "baseline_elapsed_s", "overhead_pct", "own_line_jaccard", "pairwise_task_jaccard",
+             "echo_rate", "ledger_rows", "values_sha256"]
+R23_REVIEWER = ["msgs_sent", "msgs_received", "first_delivery_t", "seal_t", "resume_fallback", "phase2_s", "stop_blocks", "hook_calls",
+                "hook_error", "hook_ms_p95", "reask_s", "attempts", "retry_s", "retry_isolated", "phase2_timeout", "p2_lines_salvaged",
+                "n_planned", "n_launched", "k", "panel_finish_at", "finish_signal_t", "finish_would_fire", "hang_kill",
+                "snapshot_missing", "late", "over_cap"]
+R23_SLOT = ["slot_type", "card_form", "deal_r", "deal_c"]
+
+
+def searcher_with_m2(p, then_cmd=None):
+    """Searcher reads source.md, makes 5 more calls (M2 injected at call 6), then optionally one more call."""
+    b = p.board
+    clock = 1000
+    b.call("t2b-1", "searcher", tool="Read", inp={"file_path": b.src})
+    for _ in range(5):
+        clock += 10
+        b.set_clock(clock)
+        out = b.call("t2b-1", "searcher")
+    assert out
+    if then_cmd:
+        b.set_clock(clock + 10)
+        b.call("t2b-1", "searcher", inp={"command": then_cmd})
+
+
+def test_pre_post_and_r23_keys(pkg1):
+    searcher_with_m2(pkg1)
+    r = pkg1.summary("pre")
+    assert r.returncode == 0, r.stderr + r.stdout
+    assert pkg1.collab_json()["ledger_rows"] is None  # pre works without ledger.json and merged-anon.md
+    (pkg1.d / "ledger.json").write_text(json.dumps({"rows": [{}, {}, {}]}))
+    assert pkg1.summary("post").returncode == 0
+    c = pkg1.collab_json()
+    assert c["ledger_rows"] == 3 and "anon_leak" in c and c["arm"] == "A6-F3"
+    for k in R23_PANEL:
+        assert k in c, k
+    for rv in c["reviewers"].values():
+        for k in R23_REVIEWER:
+            assert k in rv, k
+        assert rv["resume_fallback"] is None and rv["stop_blocks"] == 0 and rv["over_cap"] == 0 and rv["late"] == 0
+    assert c["slots"] and all(k in s for s in c["slots"] for k in R23_SLOT)
+
+
+def test_own_line_jaccard_hand_value(pkg1):
+    pkg1.review("t2b-1", report(finding()))                                            # Task 1
+    pkg1.review("t4-1", report(finding(), finding(id="F2", anchor=CAND_LONG[:60])))    # Task 1 and Task 3
+    pkg1.review("t3-1", report())                                                      # no finding
+    assert pkg1.summary("pre").returncode == 0
+    c = pkg1.collab_json()
+    assert c["task_sets"] == {"t2b-1": ["T1"], "t4-1": ["T1", "T3"], "t3-1": []}
+    assert c["own_line_jaccard"] == pytest.approx((0.5 + 0 + 0) / 3)
+
+
+@pytest.mark.parametrize("later,expect", [("grep -c x src/", True), ("ls", False)])
+def test_move_executed(pkg1, later, expect):
+    searcher_with_m2(pkg1, then_cmd=later)
+    assert pkg1.summary("pre").returncode == 0
+    slots = {s["move"]: s for s in pkg1.collab_json()["slots"]}
+    assert slots["M2"]["move_executed"] is expect
+
+
+def test_move_executed_null_for_reading_moves(pkg1):
+    b = pkg1.board
+    b.call("t4-1", "reader", tool="Read", inp={"file_path": b.src})
+    for _ in range(8):
+        b.call("t4-1", "reader")
+    assert pkg1.summary("pre").returncode == 0
+    s = [x for x in pkg1.collab_json()["slots"] if x["rid"] == "t4-1"]
+    assert s and s[0]["slot_type"] == "static" and s[0]["move_executed"] is None
+
+
+def test_elapsed_is_max_end_minus_t0(pkg1):
+    pkg1.review("t3-1", report(), end_ms=150_500)
+    assert pkg1.summary("pre").returncode == 0
+    c = pkg1.collab_json()
+    assert c["elapsed_s"] == 150.5 and c["overhead_pct"] == pytest.approx(100 * (150.5 / 116 - 1))
+
+
+def test_audit_flags_gt_substring_in_board(pkg1):
+    b = pkg1.board
+    line = {"v": "panel-msg/1", "id": "m-t4-1-08", "run": "The guard keeps every retry", "from": "radar", "to": "t4-1", "t": 1, "kind": "move", "move": "M3"}
+    (b.dir / "msgs").mkdir(exist_ok=True)
+    (b.dir / "msgs" / "radar.jsonl").write_text(json.dumps(line) + "\n")
+    (b.dir / "metrics").mkdir(exist_ok=True)
+    with (b.dir / "metrics" / "t4-1.jsonl").open("a") as f:
+        f.write(json.dumps({"ev": "inject", "id": "m-t4-1-08", "t": 1, "n": 8, "move": "M3", "slot_type": "static", "task_hint": [],
+                            "text": __import__("conftest").CAT["moves"]["M3"]}) + "\n")
+    r = pkg1.summary("pre")
+    assert r.returncode == 3 and pkg1.audit()["gt_substrings_in_board"] == 1 and (pkg1.d / "QUARANTINED").exists()
+
+
+def test_audit_flags_dirty_sandbox_and_changed_candidate(pkg1):
+    (pkg1.sb / pkg1.pkg / "repo" / "src" / "a.py").write_text("changed\n")
+    (pkg1.sb / "cand" / pkg1.pkg / "candidate.md").write_text("edited\n")
+    r = pkg1.summary("pre")
+    a = pkg1.audit()
+    assert r.returncode == 3 and a["sandbox_clean"] is False and a["candidate_sha_unchanged"] is False
+
+
+def test_collab0_coverage_from_transcripts_and_finish_would_fire(tmp_path, root):
+    p = Pkg(tmp_path, root, row="el2-c0-r0", collab=0)
+    p.run["FINISH_MS"] = 120_000
+    p.write_run()
+    p.review("t4-1", report(), end_ms=130_000)
+    tr = [{"type": "assistant", "parent_tool_use_id": None, "message": {"content": [
+        {"type": "tool_use", "name": "Bash", "input": {"command": "grep -c x src/"}}]}}]
+    (p.d / "reviews" / "t2b-1.attempt1.json").write_text(json.dumps(tr))
+    assert p.summary("pre").returncode == 0
+    c = p.collab_json()
+    assert c["arm"] == "A1" and c["moves_covered"]["M2"] == 1 and c["slots"] == []
+    assert c["reviewers"]["t4-1"]["finish_would_fire"] is True and c["reviewers"]["t2b-1"]["finish_would_fire"] is False
+    assert not (p.d / "board" / "msgs").exists() and not (p.d / "settings").exists()
+
+
+
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_anon.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_anon.py
new file mode 100644
index 000000000..aab8e8709
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_anon.py
@@ -0,0 +1,31 @@
+"""T-14: anon.sh removes every arm and reviewer marker before the judge."""
+
+import re
+
+from conftest import A1DIR, PKG, R1, TOOLS, jload, run
+
+
+def test_anon(root):
+    row = "el2-c1-r3"
+    d = root / "runs" / row / PKG
+    d.mkdir(parents=True)
+    (d / "merged-1.md").write_text(
+        f"candidate: {A1DIR}/{PKG}/candidate.md sha256 abc\n"
+        f"report {root}/runs/{row}/{PKG}/reviews/t2b-1.md, report {R1}/runs/{row}/{PKG}/reviews/t4-1.md\n"
+        f"Reviewer t3-1 and t4-1 agree with t2b-1. Sandbox /tmp/evalsb-collab-r1/{PKG}/repo/src/x.py\n"
+        '{"lid":"L1","origin":"own","claim":"x"}\n')
+    r = run(["bash", str(TOOLS / "anon.sh"), row, PKG, "--root", str(root)])
+    assert r.returncode == 0, r.stderr
+    out_dir = r.stdout.strip()
+    key = jload(d / "label-key.json")
+    assert re.fullmatch(r"[0-9a-f]{12}", key["opaque"]) and key["label"] in "QRSTUV"
+    assert out_dir == f"{root}/scoring/{key['opaque']}/{PKG}/{key['label']}"
+    text = open(f"{out_dir}/merged-anon.md").read()
+    assert not re.search(r"\bt[0-9a-z]+-[0-9]+\b", text)
+    assert "/tmp/evalsb-collab-r1" not in text and "/tmp/evalsb/" in text
+    assert "r1-move-radar" not in text.replace("<EVAL>", "") and "origin" not in text and row not in text
+    assert "candidate: <candidate file> sha256" in text and "report <redacted>" in text
+    assert "Reviewer R2 and R3 agree with R1" in text  # sorted ids t2b-1 < t3-1 < t4-1 -> R1, R2, R3
+    assert not list((root / "scoring").rglob("label-key.json"))
+    # a re-run reuses the key
+    assert run(["bash", str(TOOLS / "anon.sh"), row, PKG, "--root", str(root)]).stdout.strip() == out_dir
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_judge_path.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_judge_path.py
new file mode 100644
index 000000000..094308ab3
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_judge_path.py
@@ -0,0 +1,37 @@
+"""T-15: the unchanged judge-one.sh writes inside the tmp scoring root through the relative-path trick."""
+
+import hashlib
+import json
+import os
+
+from conftest import A1DIR, STUB_BIN, jload, run
+
+DS = "TASK-WF-designSpec-20261107-075614"
+PIN = "a01bd70d370d73cb32b55a7368aa28e2c12d93403237211c3a71f339ae82cfcc"
+
+
+def listing(p):
+    return sorted(str(x.relative_to(p)) for x in p.rglob("*"))
+
+
+def test_judge_writes_under_tmp(tmp_path):
+    judge = A1DIR / "tools" / "tmp-scripts" / "judge-one.sh"
+    assert hashlib.sha256(judge.read_bytes()).hexdigest() == PIN
+    combos = A1DIR / "arms" / "scoring" / "combos"
+    before = listing(combos)
+    opaque = tmp_path / "scoring" / "0123456789ab"
+    out = opaque / DS / "R"
+    out.mkdir(parents=True)
+    (out / "merged-anon.md").write_text("# merged\n")
+    stub = tmp_path / "stub"
+    stub.mkdir()
+    (stub / "score.body").write_text(json.dumps({"label": "R", "gt_covered_any": ["GT2"], "gt_covered_blocking": [], "wrong_blockers": 0}))
+    (stub / "plan").write_text(f"judge {stub / 'score.body'}\n")
+    c = os.path.relpath(opaque, combos)
+    env = dict(os.environ, PATH=f"{STUB_BIN}:{os.environ['PATH']}", STUB_DIR=str(stub))
+    r = run(["bash", str(judge), c, DS, "R"], env=env)
+    assert r.returncode == 0 and r.stdout.startswith("OK"), r.stdout + r.stderr
+    assert jload(out / "score.json")["gt_covered_any"] == ["GT2"] and (out / "judge.json").exists()
+    assert listing(combos) == before
+    argv = (stub / "argv.1").read_text().splitlines()
+    assert argv[argv.index("--model") + 1] == "claude-opus-5-5"
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_results.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_results.py
new file mode 100644
index 000000000..8cb1c277a
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_results.py
@@ -0,0 +1,54 @@
+"""T-16: results.py row values, null sums for an invalid package, duplicate refusal."""
+
+import json
+
+from conftest import TOOLS, jload, run
+
+DS, AL, DE = "TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"
+GT = {DS: [("GT1", True), ("GT2", True), ("GT3", False)], AL: [("GT1", True), ("GT2", False)], DE: [("GT1", False), ("GT2", False)]}
+SCORE = {DS: (["GT1", "GT2", "GT3"], ["GT1", "GT3"], 1), AL: (["GT1"], ["GT1", "GT2"], 2), DE: (["GT2"], [], 1)}
+
+
+def build(root, tmp_path, row, bad=None):
+    a1 = tmp_path / "a1"
+    for p, items in GT.items():
+        (a1 / p).mkdir(parents=True, exist_ok=True)
+        (a1 / p / "ground-truth.json").write_text(json.dumps({"items": [{"id": i, "blocking_in_implement": b} for i, b in items]}))
+        d = root / "runs" / row / p
+        (d / "reviews").mkdir(parents=True)
+        (d / "status").write_text("invalid\n" if p == bad else "ok\n")
+        (d / "label-key.json").write_text(json.dumps({"opaque": f"op{p[-6:]}", "label": "S"}))
+        (d / "collab.json").write_text(json.dumps({"elapsed_s": 120.0, "baseline_elapsed_s": 116, "ledger_rows": 4, "slots": [], "reviewers": {}}))
+        (d / "run.json").write_text(json.dumps({"k": {"searcher": 2, "reader": 2}, "values": "planning"}))
+        for rid in ("t2b-1", "t4-1", "t3-1"):
+            (d / "reviews" / f"{rid}.cost.json").write_text(json.dumps({"total_output_tokens_all": 1000}))
+        s = root / "scoring" / f"op{p[-6:]}" / p / "S"
+        s.mkdir(parents=True)
+        a, b, w = SCORE[p]
+        (s / "score.json").write_text(json.dumps({"gt_covered_any": a, "gt_covered_blocking": b, "wrong_blockers": w}))
+    return a1
+
+
+def results(root, a1, row):
+    return run(["uv", "run", "python", str(TOOLS / "results.py"), row, "--root", str(root), "--a1", str(a1)])
+
+
+def test_row_values(root, tmp_path):
+    a1 = build(root, tmp_path, "el2-c1-r3")
+    r = results(root, a1, "el2-c1-r3")
+    assert r.returncode == 0, r.stderr
+    x = jload(root / "results" / "el2-c1-r3.json")
+    assert (x["found_14"], x["real_blocking_8"], x["judge_blocking"], x["wrong_blockers"]) == (4, 2, 4, 3)
+    assert (x["control_found_2"], x["control_wrong_blockers"]) == (1, 1)
+    assert x["output_tokens"] == 9000 and x["status"] == "complete" and x["panel"] == "el2" and x["collab"] == 1 and x["rep"] == 3
+    assert x["packages"][DS]["real_blocking"] == ["GT1"]  # GT3 is judge-blocking but not blocking_in_implement
+    assert results(root, a1, "el2-c1-r3").returncode == 2  # duplicate row id refused
+    assert len((root / "results" / "results.jsonl").read_text().splitlines()) == 1
+
+
+def test_invalid_package_gives_null_sums(root, tmp_path):
+    a1 = build(root, tmp_path, "sl2-c0-r1", bad=AL)
+    assert results(root, a1, "sl2-c0-r1").returncode == 0
+    x = jload(root / "results" / "sl2-c0-r1.json")
+    assert x["status"] == "incomplete" and x["found_14"] is None and x["output_tokens"] is None
+    assert x["control_found_2"] == 1  # DE alone is still ok
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_alarms.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_alarms.py
new file mode 100644
index 000000000..0042ffd9a
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_alarms.py
@@ -0,0 +1,45 @@
+"""T-18 and F-2: arm-level alarms."""
+
+import json
+
+from conftest import TOOLS, run
+
+P = "TASK-WF-designSpec-20261107-075614"
+
+
+def row(collab, rep, jac=0.2, ledger=10, elapsed=116.0, b_f=116.0, inj=None, snap=0, receivers=3):
+    return {"row": f"el2-c{collab}-r{rep}", "panel": "el2", "collab": collab, "rep": rep,
+            "packages": {P: {"status": "ok", "ledger_rows": ledger, "elapsed_s": elapsed, "B_f": b_f, "overhead_pct": 100 * (elapsed / b_f - 1)}},
+            "collab_counters": {"own_line_jaccard": {P: jac}, "injections_by_move": inj or {"M2": 1}, "snapshot_missing": snap, "receivers": receivers}}
+
+
+def alarms(root, rows):
+    (root / "results").mkdir(exist_ok=True)
+    (root / "results" / "results.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
+    r = run(["uv", "run", "python", str(TOOLS / "alarms.py"), "el2", "--root", str(root)])
+    assert r.returncode == 0, r.stderr
+    return json.loads(r.stdout), r.stderr
+
+
+def test_convergence_slo_and_drift(root):
+    rows = [row(0, 1), row(0, 2), row(0, 3, elapsed=140.0),                     # collab-0 mean Jaccard 0.2, ledger 10
+            row(1, 1, jac=0.4), row(1, 2, ledger=7), row(1, 3, elapsed=170.0),  # jaccard fire, ledger fire, slow package
+            row(1, 0, jac=0.9)]                                                 # rep 0 (smoke) is ignored
+    rep, _ = alarms(root, rows)
+    fired = {f["row"] for f in rep["convergence"]["fired"]}
+    assert fired == {"el2-c1-r1", "el2-c1-r2"}
+    assert rep["arms"]["collab1"]["slo_spent"] == [["el2-c1-r3", P]]  # 170 > 1.35 x B_c (median 116)
+    used = {b["rep"]: b["used"] for b in rep["blocks"]}
+    assert used == {1: True, 2: True, 3: False}  # block 3: drift 140/116 = 1.21 > 1.10
+
+
+def test_snapshot_alarm(root):
+    rep, _ = alarms(root, [row(0, 1), row(1, 1, snap=2)])
+    assert rep["snapshot"]["fired"] == ["el2-c1-r1"]
+
+
+def test_f2_same_gaps_reported_not_failed(root):
+    rows = [row(0, i) for i in range(1, 6)] + [row(1, i, inj={"M2": 1, "M3": 2}) for i in range(1, 6)]
+    rep, err = alarms(root, rows)
+    assert rep["same_gaps"] is True and "SAME_GAPS" in err
+    assert rep["arms"]["collab1"]["injections_by_move"] == {"M2": 5, "M3": 10}
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_cleanup.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_cleanup.py
new file mode 100644
index 000000000..be3cdcbe1
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_cleanup.py
@@ -0,0 +1,22 @@
+"""T-19: cleanup removes only the session files of its own row (R-46)."""
+
+import json
+
+from conftest import PKG, TOOLS, run
+
+
+def test_cleanup_only_own_row(root, tmp_path):
+    sb = tmp_path / "sb"
+    proj = tmp_path / "projects"
+    enc = "".join(c if c.isalnum() else "-" for c in f"{sb}/{PKG}/repo")
+    (proj / enc).mkdir(parents=True)
+    for row, sid in (("el2-c1-r1", "aaa"), ("el2-c0-r1", "bbb")):
+        rv = root / "runs" / row / PKG / "reviews"
+        rv.mkdir(parents=True)
+        (rv / "t4-1.meta.json").write_text(json.dumps({"session_ids": [sid]}))
+        (proj / enc / f"{sid}.jsonl").write_text("{}\n")
+    (proj / enc / "aaa-dir.jsonl").mkdir()  # never a directory
+    r = run(["bash", str(TOOLS / "cleanup-sessions.sh"), "el2-c1-r1", "--root", str(root), "--sb", str(sb), "--projects", str(proj)])
+    assert r.returncode == 0, r.stderr
+    assert not (proj / enc / "aaa.jsonl").exists() and (proj / enc / "bbb.jsonl").exists() and (proj / enc / "aaa-dir.jsonl").is_dir()
+    assert "DELETED" in (root / "runs" / "el2-c1-r1" / "cleanup.log").read_text()
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py
deleted file mode 100644
index 138dab799..000000000
--- a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py
+++ /dev/null
@@ -1,84 +0,0 @@
-"""Fault-injection tests F-1..F-14 (DESIGN.md section 6.2)."""
-
-import json
-
-from conftest import ctx_text
-
-
-# F-6: snapshot failure -> snapshot_missing 1, zero deliveries (same mechanism as T-7)
-def test_f6_snapshot_failure(board, tmp_path):
-    outs = [board.call("t4-1", "reader", transcript=tmp_path / "nope.jsonl") for _ in range(13)]
-    assert all(o == "" for o in outs)
-    assert len(board.events("t4-1", "snapshot_missing")) == 1 and board.events("t4-1", "inject") == []
-
-
-# F-7: a garbage line in tele/ does not change the hook's output
-def test_f7_corrupt_board_line(board, tmp_path):
-    from conftest import Board
-    clean = Board(tmp_path / "clean")
-    board.tele("t2b-1", "\x00garbage{")
-    a = [board.call("t2b-1", "searcher") for _ in range(10)]
-    b = [clean.call("t2b-1", "searcher") for _ in range(10)]
-    assert [bool(x) for x in a] == [bool(x) for x in b] and ctx_text(a[9]) == ctx_text(b[9])
-
-
-# F-14: env -i PATH=/usr/bin:/bin gives the same decisions and outputs
-def test_f14_environment_cleared(board, tmp_path):
-    from conftest import Board
-    other = Board(tmp_path / "envi")
-    env = {"PATH": "/usr/bin:/bin"}
-    a = [board.call("t2b-1", "searcher") for _ in range(11)]
-    b = [other.call("t2b-1", "searcher", env=env) for _ in range(11)]
-    assert a == b
-    strip = lambda evs: [{k: v for k, v in e.items() if k not in ("ms",)} for e in evs if e["ev"] != "t"]  # noqa: E731
-    assert strip(board.metrics("t2b-1")) == strip(other.metrics("t2b-1"))
-    assert json.loads(a[5]) and json.loads(a[9])
-
-
-# ---------------------------------------------------------------- runner faults (stub claude)
-def test_f8_hang_killed_at_deadline(runner):
-    import time
-    for collab in (1, 0):
-        if collab:
-            runner.settings("t2b-1")
-        runner.write_run(hang_ms=int(time.time() * 1000) + 3000)
-        (runner.stub / "count").unlink(missing_ok=True)
-        runner.plan("sleep 60")
-        t = time.time()
-        r = runner.run(collab=collab)
-        took = time.time() - t
-        assert r.returncode == 1 and took < 3 + 5 + 3  # TERM at the deadline, KILL at most 5 s later (+ start-up)
-        m = runner.meta()
-        assert m["hang_kill"] is True and m["valid"] is False and runner.calls() == 1  # no time left for a retry
-
-
-def test_f9_failed_block_then_isolated_retry(runner):
-    from conftest import finding, json_reply, report
-    runner.settings("t2b-1")
-    runner.plan(f"replay {runner.file(json_reply('incomplete'))}", f"replay {runner.file(json_reply(report(finding())))}")
-    assert runner.run(collab=1).returncode == 0
-    m = runner.meta()
-    assert m["attempts"] == 2 and m["retry_isolated"] is True and "--settings" not in runner.argv(2)
-
-
-def test_f10_binary_missing_twice(runner):
-    runner.plan("exit 127")
-    r = runner.run(collab=0)
-    assert r.returncode == 1 and runner.calls() == 2
-    assert all(runner.argv(k)[runner.argv(k).index("--model") + 1] == "muse-ember-1.0" for k in (1, 2))
-    assert runner.meta()["valid"] is False and not (runner.d / "reviews" / "t2b-1.fallback.log").exists()
-
-
-def test_f13_hook_error_does_not_kill_review(runner, tmp_path):
-    """The stub runs the real hook from --settings for 8 tool calls; the hook's inputs break mid-run."""
-    from conftest import Board, finding, json_reply, report
-    b = Board(tmp_path / "f13")
-    s = runner.settings("t2b-1", board=str(b.dir))
-    assert str(b.dir) in s
-    (b.dir / "ctx" / "index.json").write_text("{broken")  # every checkpoint now fails inside the hook
-    runner.plan(f"hooks 8 {runner.file(json_reply(report(finding())))}")
-    r = runner.run(collab=1)
-    assert r.returncode == 0, r.stderr
-    assert runner.meta()["valid"] is True
-    assert [m for m in b.metrics("t2b-1") if m["ev"] == "hook_error"]
-    assert all(x == "rc=0" for x in (runner.stub / "hook-rc.1").read_text().split())
diff --git a/dev/fd/63 b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py
index 000000000..3ff37126f 100644
--- a/dev/fd/63
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_faults.py
@@ -82,3 +82,65 @@ def test_f13_hook_error_does_not_kill_review(runner, tmp_path):
     assert runner.meta()["valid"] is True
     assert [m for m in b.metrics("t2b-1") if m["ev"] == "hook_error"]
     assert all(x == "rc=0" for x in (runner.stub / "hook-rc.1").read_text().split())
+
+
+# ---------------------------------------------------------------- summary faults (collab_summary.py)
+def test_f1_classifier_mislabel_listed(pkg1):
+    """The live index lost its keys/paths, so a real M1 call by a peer is missed live and M1 is injected anyway."""
+    import json as _j
+
+    from conftest import FIX
+    b = pkg1.board
+    ix = _j.loads((FIX / "index.json").read_text())
+    ix["paths"], ix["keys"] = ["nothing/here.py"], ["zzzz"]
+    (b.dir / "ctx" / "index.json").write_text(_j.dumps(ix))
+    b.tele("t4-1", _j.dumps({"n": 1, "t": 0, "rid": "t4-1", "sub": False, "tool": "Bash", "input": {"command": "grep -rln merge_guard tests/"}}))
+    b.call("t2b-1", "searcher", tool="Read", inp={"file_path": b.src}, order="M1,M2,M7,M4")
+    for _ in range(5):
+        out = b.call("t2b-1", "searcher", order="M1,M2,M7,M4")
+    assert "No panel member" in out and b.events("t2b-1", "inject")[0]["move"] == "M1"
+    assert pkg1.summary("pre").returncode == 0
+    spot = pkg1.audit()["spot_check"]
+    assert any(s.get("move") == "M1" and s["post_hoc"] == "covered" for s in spot)
+
+
+def test_f3_reviewer_ignores_injection(pkg1):
+    from test_collab_summary import searcher_with_m2
+    searcher_with_m2(pkg1, then_cmd="ls -la")
+    assert pkg1.summary("pre").returncode == 0
+    s = [x for x in pkg1.collab_json()["slots"] if x["move"] == "M2"][0]
+    assert s["move_executed"] is False
+    assert sum(1 for x in pkg1.collab_json()["slots"] if x["move_executed"] is True) == 0
+
+
+def _plant(p, line, text, inject_id=None):
+    import json as _j
+    b = p.board
+    (b.dir / "msgs").mkdir(exist_ok=True)
+    if line is not None:
+        (b.dir / "msgs" / "radar.jsonl").write_text(_j.dumps(line) + "\n")
+    if inject_id:
+        (b.dir / "metrics").mkdir(exist_ok=True)
+        with (b.dir / "metrics" / "t4-1.jsonl").open("a") as f:
+            f.write(_j.dumps({"ev": "inject", "id": inject_id, "t": 1, "n": 8, "move": "M3", "slot_type": "static", "task_hint": [], "text": text}) + "\n")
+
+
+def test_f4_leak_quarantines(tmp_path, root):
+    from conftest import CAT, Pkg
+    base = {"v": "panel-msg/1", "id": "m-t4-1-08", "run": "r", "from": "radar", "to": "t4-1", "t": 1, "kind": "move", "move": "M3"}
+    cases = [(dict(base, anchor="Create the guard"), CAT["moves"]["M3"], "m-t4-1-08"),   # an anchor key
+             (base, CAT["moves"]["M3"] + " Look at Task 3.", "m-t4-1-08"),                # text differs from the catalogue
+             (base, None, None)]                                                         # board line, no inject event
+    for i, (line, text, iid) in enumerate(cases):
+        p = Pkg(tmp_path / f"c{i}", root, row=f"el2-c1-r{i + 1}")
+        _plant(p, line, text, iid)
+        r = p.summary("pre")
+        assert r.returncode == 3, (i, r.stdout, r.stderr)
+        assert (p.d / "QUARANTINED").read_text().strip()
+
+
+def test_f8_slo_breach_from_hang(pkg1):
+    pkg1.review("t4-1", "", end_ms=179_000, hang_kill=True, valid=False)
+    assert pkg1.summary("pre").returncode == 0
+    c = pkg1.collab_json()
+    assert c["slo_breach"] is True and c["reviewers"]["t4-1"]["hang_kill"] is True

Codegraph context
index_state=fresh checked_at=2026-11-13T20:27:49Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b: the changed files are shell, jq, JSON and Python under .dev (eval harness, no product symbols have dependents outside the touched set); dependents checked on the Grep/Read floor: none outside the touched set.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
