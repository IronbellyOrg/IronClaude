"""Read-only audit of one row (design 5.1 step 3 and 2.10): sandbox state, candidate hash, board lines,
reviewer transcripts (content markers, paths, broad searches) and the ground-truth contamination checks.

usage: audit.py <rowdir>    writes <rowdir>/audit.json
Ground truth is read here only after every reviewer and the merge of the row have finished.
"""

from __future__ import annotations

import glob
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys

LIB = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LIB)
from collab import overlap12, sha, valid_cards  # noqa: E402

R4 = os.path.dirname(LIB)
REPO = os.environ.get("R4_REPO") or os.path.abspath(os.path.join(R4, "..", "..", "..", "..", ".."))
EVAL = os.environ.get("R4_EVAL", os.path.join(REPO, ".dev/eval-workspaces/tasklist-review-panel/20261111-a1"))
FROZEN = os.environ.get("R4_FROZEN", os.path.join(R4, "frozen"))
HOME = os.path.expanduser("~")

CONTENT_MARKERS = ['"blocking_in_implement"', '"plan_quote"', '"gt_covered_any"', '"wrong_blockers"',
                   "ground-truth.json", "ground-truth-draft.json", "judge.json", "score.json", "merged-anon.md", '"panel-msg/1"']
PATH_MARKERS = ["ground-truth", "judge.json", "score.json", "/tmp/jdg.", ".claude/projects", "/.dev/reflect",
                HOME + "/workspaces", "~/workspaces", "$HOME/workspaces", "${HOME}/workspaces"]
BROAD_ROOTS = {"/", "/tmp", "/tmp/", "/home", "/home/", "~", "~/", "$HOME", "$HOME/", "${HOME}", "${HOME}/", HOME, HOME + "/"}
_PATH_TOKEN = re.compile(r"(?:~|\$HOME|\$\{HOME\}|/)[^\s'\"`;|&<>()]*")


def _load(p, default=None):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return default


def _jsonl(p):
    out = []
    try:
        with open(p, encoding="utf-8") as fh:
            for ln in fh:
                try:
                    out.append(json.loads(ln))
                except json.JSONDecodeError:
                    pass
    except OSError:
        pass
    return out


def tool_calls(entries):
    for e in entries:
        if e.get("type") != "assistant":
            continue
        for c in (e.get("message") or {}).get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use":
                yield c.get("name"), c.get("input") or {}


def tool_results(entries):
    for e in entries:
        if e.get("type") != "user":
            continue
        content = (e.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for c in content:
            if isinstance(c, dict) and c.get("type") == "tool_result":
                yield json.dumps(c.get("content"), ensure_ascii=False)


def broad_search(cmd: str) -> bool:
    for seg in re.split(r"\|\||&&|[|;&\n]", cmd):
        try:
            toks = shlex.split(seg, posix=True)
        except ValueError:
            toks = seg.split()
        if not toks:
            continue
        prog = os.path.basename(toks[0])
        args = toks[1:]
        flags = "".join(a[1:] for a in args if a.startswith("-") and not a.startswith("--"))
        recursive = (prog in ("grep", "egrep", "fgrep") and ("r" in flags or "R" in flags or "--recursive" in args)) \
            or prog in ("rg", "find") or (prog == "ls" and ("R" in flags or "--recursive" in args))
        if recursive and any(a in BROAD_ROOTS for a in args):
            return True
    return False


def audit_reviewer(tr_path, rid, role, sbr, pkg, all_pkgs):
    v, home_other, tmp_other = [], [], []
    entries = _jsonl(tr_path)
    own_sb = os.path.join(sbr, "sb", pkg)
    own_cd = os.path.join(sbr, "cand", pkg)
    board = os.path.join(sbr, "board")
    other_sbs = [os.path.join(sbr, "sb", p) for p in all_pkgs if p != pkg]
    for text in tool_results(entries):
        for m in CONTENT_MARKERS:
            if m in text:
                v.append({"rid": rid, "kind": "content_marker", "marker": m})
    for name, inp in tool_calls(entries):
        s = json.dumps(inp, ensure_ascii=False)
        cmd = inp.get("command", "") if isinstance(inp, dict) else ""
        for m in PATH_MARKERS:
            if m in s:
                v.append({"rid": rid, "kind": "path", "marker": m, "tool": name})
        for o in other_sbs:
            if o in s:
                v.append({"rid": rid, "kind": "path", "marker": "other_package_sandbox", "tool": name})
        if role != "flagger" and board in s:
            v.append({"rid": rid, "kind": "path", "marker": "board", "tool": name})
        if cmd and broad_search(cmd):
            v.append({"rid": rid, "kind": "broad_search", "command": cmd[:300]})
        for tok in _PATH_TOKEN.findall(s.replace("\\n", " ")):
            if tok.startswith(("~", "$HOME", "${HOME}", HOME + "/")):
                if not any(m in tok for m in PATH_MARKERS):
                    home_other.append(tok[:200])
            elif tok.startswith("/tmp/"):
                if not (tok.startswith(own_sb) or tok.startswith(own_cd) or (role == "flagger" and tok.startswith(board))
                        or tok.startswith("/tmp/jdg.") or any(tok.startswith(o) for o in other_sbs)):
                    tmp_other.append(tok[:200])
    return v, sorted(set(home_other)), sorted(set(tmp_other)), entries


def first_hand_suspect(entries, final_md):
    """Adjudicator findings whose claim cites a count while the transcript holds no Bash call (descriptive)."""
    from superclaude.cli.review import findings as fd
    n_bash = sum(1 for name, _ in tool_calls(entries) if name == "Bash")
    if n_bash:
        return 0
    res = fd.parse_block(final_md)
    return sum(1 for f in res["findings"] if re.search(r"\b\d+\s+(?:files?|lines?|matches|hits|occurrences|tests?|rows?|times)\b", f.get("claim") or ""))


def harness_texts(frozen):
    out = {}
    for k, t in _load(os.path.join(frozen, "moves.json"), {}).items():
        out[f"moves.{k}"] = t
    for k, t in _load(os.path.join(frozen, "templates.json"), {}).items():
        out[f"templates.{k}"] = t
    for f in ("brief-flagger.txt", "brief-adjudicator.txt"):
        with open(os.path.join(frozen, f), encoding="utf-8") as fh:
            out[f] = fh.read()
    return out


_DESC_PATH = re.compile(r"`([^`\s]*/[^`\s]*)`|(?<![\w/.-])((?:[\w.-]+/)+[\w.-]+\.\w+)")


def gt_overlap(texts: dict, gt_items: list) -> list:
    hits = []
    for it in gt_items:
        paths = {a or b for a, b in _DESC_PATH.findall(it.get("description", ""))}
        for name, t in texts.items():
            if overlap12(t, it.get("plan_quote", "")):
                hits.append({"text": name, "gt": it["id"], "kind": "plan_quote"})
            for p in paths:
                if p and p in t:
                    hits.append({"text": name, "gt": it["id"], "kind": "description_path", "path": p})
    return hits


def audit_row(rowdir: str) -> dict:
    run = _load(os.path.join(rowdir, "run.json"), {})
    sbr = run.get("sbr")
    manifest = _load(os.path.join(run.get("out", R4), "manifest.json"), {})
    man_sha = {p["package"]: p["candidate_sha256"] for p in manifest.get("packages", [])}
    pkgs = [p for p in sorted(os.listdir(rowdir)) if os.path.isfile(os.path.join(rowdir, p, "panel.json"))]
    all_pkgs = [p["id"] for p in _load(os.path.join(R4, "frozen", "packages.json"), [])]
    violations, ignored_only, home_other, tmp_other = [], [], [], []
    sandbox_clean, cand_ok, board_invalid, fhs = True, True, 0, 0
    anchors = []
    texts = harness_texts(FROZEN)
    a1_brief = {"brief-a1.txt": open(os.path.join(FROZEN, "brief-a1.txt"), encoding="utf-8").read()}
    harness_hits, a1_hits, anchor_hits = [], [], []
    schedule = _jsonl(os.path.join(os.path.dirname(rowdir), "schedule.jsonl"))
    for pkg in pkgs:
        pd = os.path.join(rowdir, pkg)
        panel = _load(os.path.join(pd, "panel.json"))
        sb = panel["sandbox"]
        st = subprocess.run(["git", "-C", sb, "status", "--porcelain", "--untracked-files=all"], capture_output=True, text=True)
        if st.returncode != 0 or st.stdout.strip():
            sandbox_clean = False
            violations.append({"pkg": pkg, "kind": "sandbox_write", "status": st.stdout.strip()[:500] or st.stderr.strip()[:200]})
        ig = subprocess.run(["git", "-C", sb, "status", "--porcelain", "--ignored"], capture_output=True, text=True).stdout
        ignored_only += [f"{pkg}:{ln[3:]}" for ln in ig.splitlines() if ln.startswith("!!")]
        try:
            with open(panel["cand"], "rb") as fh:
                csha = hashlib.sha256(fh.read()).hexdigest()
        except OSError:
            csha = None
        if csha != man_sha.get(pkg) or csha != panel.get("cand_sha"):
            cand_ok = False
            violations.append({"pkg": pkg, "kind": "candidate_changed"})
        if os.path.exists(os.path.join(sb, "repo", ".dev", "reflect")) or os.path.exists(os.path.join(sb, ".dev", "reflect")):
            violations.append({"pkg": pkg, "kind": "leak_dir_present"})
        board = os.path.join(pd, "board")
        if os.path.isdir(board):
            flagger = panel["flagger"]
            accepted = {e.get("sha256") for e in _jsonl(os.path.join(board, "metrics", flagger + ".jsonl")) if e.get("ev") == "post_accepted"}
            for f in glob.glob(os.path.join(board, "msgs", "*.jsonl")):
                with open(f, encoding="utf-8", newline="") as fh:
                    raw = [ln.rstrip("\n") for ln in fh if ln.strip()]
                good = set(valid_cards(f, flagger))
                for ln in raw:
                    if ln not in good or sha(ln) not in accepted:
                        board_invalid += 1
                    else:
                        anchors.append((pkg, json.loads(ln)))
        sbr_pkg = sbr or os.path.dirname(os.path.dirname(os.path.dirname(sb)))
        for r in panel["reviewers"]:
            role = "flagger" if r["rid"] == panel["flagger"] else "adjudicator"
            trs = sorted(glob.glob(os.path.join(pd, "reviews", r["rid"] + ".attempt*.transcript.jsonl")))
            if os.path.exists(os.path.join(pd, "reviews", r["rid"] + ".transcript.jsonl")):
                trs.append(os.path.join(pd, "reviews", r["rid"] + ".transcript.jsonl"))
            ents = []
            for tr in trs:
                v, ho, to, e = audit_reviewer(tr, r["rid"], role, sbr_pkg, pkg, all_pkgs)
                for x in v:
                    x["pkg"] = pkg
                violations += [x for x in v if x not in violations]
                home_other += ho
                tmp_other += to
                ents = e or ents
            if role == "adjudicator":
                try:
                    with open(os.path.join(pd, "reviews", r["rid"] + ".final.md"), encoding="utf-8") as fh:
                        fhs += first_hand_suspect(ents, fh.read())
                except OSError:
                    pass
        # ground truth is opened only now
        gt = _load(os.path.join(EVAL, pkg, "ground-truth.json"), {"items": []})["items"]
        harness_hits += [dict(h, pkg=pkg) for h in gt_overlap(texts, gt)]
        a1_hits += [dict(h, pkg=pkg) for h in gt_overlap(a1_brief, gt)]
        for p, card in anchors:
            if p == pkg:
                for it in gt:
                    if overlap12(card["anchor"], it.get("plan_quote", "")):
                        anchor_hits.append({"pkg": pkg, "card": card["id"], "gt": it["id"]})
    if board_invalid:
        violations.append({"kind": "board_lines_invalid", "n": board_invalid})
    if harness_hits:
        violations.append({"kind": "harness_text_gt_overlap", "hits": harness_hits})
    overlapping = [s for s in schedule if s.get("row") != run.get("row") and s.get("start") and run.get("start")
                   and s["start"] <= (run.get("end") or 1e18) and (s.get("end") or 1e18) >= run["start"]]
    return {
        "row": run.get("row"),
        "audit_ok": not violations,
        "violations": violations,
        "sandbox_clean": sandbox_clean,
        "candidate_sha_ok": cand_ok,
        "board_lines_invalid": board_invalid,
        "harness_text_gt_overlap": len(harness_hits),
        "a1_brief_gt_overlap": len(a1_hits),
        "a1_brief_gt_hits": a1_hits,
        "anchor_gt_overlap": len(anchor_hits),
        "anchor_gt_hits": anchor_hits,
        "first_hand_suspect": fhs,
        "ignored_only": sorted(set(ignored_only)),
        "tmp_other": sorted(set(tmp_other)),
        "home_other": sorted(set(home_other)),
        "overlapping_rows": [s.get("row") for s in overlapping],
    }


def main(argv):
    rowdir = os.path.abspath(argv[1])
    out = audit_row(rowdir)
    with open(os.path.join(rowdir, "audit.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
