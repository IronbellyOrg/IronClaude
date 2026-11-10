#!/usr/bin/env python3
"""A/B harness ab1: three independent first reviews, deterministic MERGE, verify gate (VF1-VF3).

Usage (run with `uv run --no-project python harness.py ...`):
  build [--stratum sonnet|haiku] [--extend]   create sandboxes (b1-r1..r6 | b1h-r1..r4 | b1-r7..r9)
  prep RUN STEP [K=V ...]                      write RUN/PROMPT-STEP.md
  ingest RUN STEP                              record outputs of a finished step
  setids RUN STEP "F1, F2"                     manual blocking ids for a report
  unlaunch RUN STEP                            drop a launch ledger entry (relaunch once, then the run is lost)
  status | tokens | basetokens | analyze
Cost rule (owner decision D6): nothing here stops, skips or truncates a run because of token cost.
Cost is evaluated only in `analyze`, after runs are complete."""
import collections
import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import score_themes as sc  # noqa: E402
from score_themes import ids_from, parse_ids, blocking_findings  # noqa: E402,F401

S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S / "scratchpad"
P11 = SP / "p11"
P12 = SP / "p12"
AB = P12 / "ab1"
RUNS = AB / "runs"
REPO = str(AB / "repo")                       # git_show reads the private clone
BASE_REF = "69ac8b3335564fb5551980e984c5d9b763039cc1"   # frozen audit command
PRODUCT_REF = "44f37e16d335a322e618b24c16ba387ffdfb47a1"       # test-arm command + rules file (set after the A4 commit)
SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
AUD_CMD_SHA = "e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494"
AUD_RULES_SHA = "3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8"
TASKS_GLOB = os.environ.get("AB_TASKS_GLOB", "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output")
MAX_CONCURRENT = int(os.environ.get("AB_MAX", "6"))
DESIGN = "b1"
S1 = SP / "exp346/.dev/experiments/346-validation/phase2/S1"
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
HIST = f"{D}/specs/history"
REVIEW = f"{D}/review"
FLAGS = "--mode critique --focus requirements,architecture"
AUD_OUT = f"{D}/review/audit.md"
R1S = ["R1a", "R1b", "R1c"]
STEPS = ["R1a", "R1b", "R1c", "VF1", "V1", "R2", "VF2", "V2", "R3", "VF3", "AUD", "AUD2"]
LOOP_STEPS = [s for s in STEPS if s not in ("AUD", "AUD2")]
OUT = {"R1a": f"{REVIEW}/round1.md", "R1b": f"{REVIEW}/round1.md", "R1c": f"{REVIEW}/round1.md",
       "VF1": f"{REVIEW}/verify-1.md", "V1": f"{REVIEW}/revise1.md", "R2": f"{REVIEW}/round2.md",
       "VF2": f"{REVIEW}/verify-2.md", "V2": f"{REVIEW}/revise2.md", "R3": f"{REVIEW}/round3.md",
       "VF3": f"{REVIEW}/verify-3.md", "AUD": AUD_OUT, "AUD2": AUD_OUT}
DROP_RE = re.compile(r"(?i)^\s*(?:[-*]\s*)?(?:\*\*)?\s*(recommendation|rationale|experts?|priority|quality impact|why blocking|suggested fix)\b")
VERIFY_BLOCK = ("> verification (coordinator, VERIFY step VF{n}; verifier reply " + REVIEW + "/verify-{n}.md): "
                "confirmed blocking ids: {c}. Rejected, kept as noted, unactioned and not prior blocking findings for the next "
                "re-review: {r}. The Reviser brief below is narrowed to the confirmed ids.")
REVISER_RULES = ("Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; "
                 "add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; "
                 "prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.")


def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
def git_show(ref, path): return subprocess.run(["git", "-C", REPO, "show", f"{ref}:{path}"], check=True, capture_output=True, text=True).stdout
def run_dir(run): return RUNS / run
def arm_of(run): return 3
def load(run): return json.load(open(run_dir(run) / "state.json"))
def save(run, st): json.dump(st, open(run_dir(run) / "state.json", "w"), indent=1)
def ws(run): return run_dir(run) / "ws"
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def sha_text(t): return hashlib.sha256(t.encode()).hexdigest()
def all_runs(): return sorted((p.name for p in RUNS.iterdir() if (p / "state.json").exists()), key=run_sort) if RUNS.exists() else []
def run_sort(run):
    m = re.match(r"b1(h?)-r(\d+)$", run)
    return (1 if m and m.group(1) else 0, int(m.group(2)) if m else 0)
def decision(): return json.load(open(AB / "decision.json"))


def spec_stats(base):
    b = (pathlib.Path(base) / SPEC).read_bytes()
    return {"bytes": len(b), "lines": b.count(b"\n"), "sha256": hashlib.sha256(b).hexdigest()}


def section(text, title):
    m = re.search(rf"^### {re.escape(title)}\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    return m.group(1).strip()


def sandbox(step_dir, run_dir_, cmd_text, rules_text):
    """Fresh arm-3 sandbox: overlay copy, review/, specs/history/, rules file under home, command.md."""
    d = pathlib.Path(step_dir)
    (d / "home/.claude/rules/prompts").mkdir(parents=True)
    shutil.copytree(S1 / "inputs/repo-overlay", d / "ws")
    (d / "ws" / D / "review").mkdir(parents=True)
    (d / "ws" / D / "specs/history").mkdir(parents=True)
    (d / "command.md").write_text(cmd_text)
    (d / "home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules_text)
    assert sha(d / "ws" / SPEC) == SPEC_SHA, "spec hash mismatch"


def run_names(stratum, extend):
    if stratum == "haiku":
        return [f"b1h-r{i}" for i in range(1, decision()["N_HAIKU"] + 1)]
    if extend:
        n = decision()["N_SONNET"]
        return [f"b1-r{i}" for i in range(n + 1, n + decision()["N_EXTEND"] + 1)]
    return [f"b1-r{i}" for i in range(1, decision()["N_SONNET"] + 1)]


def build(stratum="sonnet", extend=False):
    if extend:
        if stratum != "sonnet":
            raise SystemExit("--extend is Sonnet only")
        mp = AB / "metrics.json"
        m = json.load(open(mp)) if mp.exists() else {}
        sm = m.get("sonnet", {})
        if not (sm.get("n_runs") == decision()["N_SONNET"] and sm.get("extension_eligible")):
            raise SystemExit("--extend refused: metrics.json does not record a Sonnet n=6 outcome of INCONCLUSIVE")
        if (RUNS / f"b1-r{decision()['N_SONNET'] + 1}").exists():
            raise SystemExit("--extend refused: already extended once (never extend twice without the owner)")
    cmd = git_show(PRODUCT_REF, "src/superclaude/commands/spec-panel.md")
    rules = git_show(PRODUCT_REF, "src/superclaude/rules/prompts/document_review_loop_prompts.md")
    for run in run_names(stratum, extend):
        d = run_dir(run)
        if d.exists():
            print("skip existing", run)
            continue
        sandbox(d, d, cmd, rules)
        for x in "abc":
            sandbox(d / f"r1{x}", d, cmd, rules)
        save(run, {"run": run, "design": DESIGN, "rep": int(run.split("-r")[1]), "stratum": stratum, "loop_model": stratum,
                   "product_ref": PRODUCT_REF, "cmd_sha": sha_text(cmd), "rules_sha": sha_text(rules),
                   "done": [], "prepared": [], "transitioned": [], "log": {}, "launched": {}, "noted_unactioned": [],
                   "loop_end": None, "manual": [], "relaunch": {}, "lost": False, "complete": False, "merge": {}})
    print("built", sorted(p.name for p in RUNS.iterdir()))


# ---------------------------------------------------------------- briefs (arm-3 strings, unchanged from Stage 2)
CTX = (f"First read {D}/README.md (binding shared context; the files under {D}/inventory/ are the only evidence you can check, "
       f"mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file(s).")
RULES_PTR = "~/.claude/rules/prompts/document_review_loop_prompts.md"


def brief_first(out):
    return f"Run /sc:spec-panel @{SPEC} {FLAGS} . Review per the FIRST-REVIEW prompt in {RULES_PTR}. Values: candidate={SPEC}.\nWrite the full report to {out}. Do not edit anything else. {CTX}"


def brief_re(prior, base, out):
    return (f"Run /sc:spec-panel @{SPEC} {FLAGS} --re-review {prior} --baseline {base} . Re-review per the RE-REVIEW prompt in {RULES_PTR}. "
            f"Values: candidate={SPEC}, baseline={base}, prior={prior}.\nWrite the full report to {out}. Do not edit anything else. {CTX}")


def brief_revise(ids, rep, out):
    return (f"Revise per the REVISE prompt in {RULES_PTR}. Values: candidate={SPEC}, IDS={ids}.\n"
            f"Inputs: the review report {rep} (its Reviser brief lists the blocking ids), the spec, and the files under {D}/inventory/. "
            f"Edit the spec {SPEC} in place; it is the only file you may change besides your output. Do not run the spec-panel. "
            f"Write {out} with the byte accounting the prompt asks for and one row per finding id (applied where, or rejected with a cited reason). {CTX}")


def audit_brief():
    return (f"Run /sc:spec-panel @{SPEC} {FLAGS} . This is a labelled whole-document audit of the final spec: a first review of the whole document. "
            f"Review per the FIRST-REVIEW prompt in {RULES_PTR}. Values: candidate={SPEC}.\n"
            f"Write the full report to {AUD_OUT}. Do not edit anything else. First read {D}/README.md (binding shared context; the files under {D}/inventory/ "
            f"are the only evidence you can check, mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file.")


WRAP = """You are a worker in a controlled experiment. Follow these rules exactly.

SANDBOX: work ONLY inside {sb}. Do not read, list, search or write any path outside that directory (no parent directories, no sibling directories, no other part of the filesystem, no git history).

WORKSPACE: the directory {sb}/{wsdir} is the repo root for this task. Relative paths in the brief (such as .dev/orca-command-refactor/...) resolve there. There is no Orca, no live repository and no worker_done in this sandbox; a path:line citation you cannot check against a file inside the workspace is UNVERIFIED.

HOME: for this task the shell home `~` resolves to {sb}/home. Files under {sb}/home are inside the sandbox and may be read; a path written with `~` means the same path under it.
{cmdpart}
TOOLS: you may use Read, Grep, Glob, Edit, Write and Bash inside the sandbox. Edit or write only the files the brief assigns to you.

BRIEF (verbatim, from the coordinator):
{brief}

FINAL REPLY: after your output file is written, reply with only `DONE <path of your output file>`. Do not paste the report or any other text.
"""
CMDPART = """
COMMAND: you cannot run slash commands. The file {sb}/command.md is the definition of the /sc:spec-panel command. Act as that command: apply its critique mode, its "Review Loop" section and its "Mandatory Output Artifacts" exactly as written, and every other section of it that applies. Read command.md in full first.
"""


def wrap(sb, brief, cmd):
    return WRAP.format(sb=sb, wsdir="ws", cmdpart=CMDPART.format(sb=sb) if cmd else "", brief=brief)


# ---------------------------------------------------------------- ids / manual ids
def manual_ids(st, step):
    for m in reversed(st.get("manual", [])):
        if m["step"] == step:
            return m["ids"]
    return None


def step_report(run, step):
    """Absolute path of the review report of a review step as used by the loop."""
    if step in R1S:
        return ws(run) / REVIEW / f"round1-{step[-1].lower()}.md"
    n = {"R2": 2, "R3": 3}[step]
    return ws(run) / REVIEW / f"round{n}.md"


def step_ids(run, step, path=None):
    st = load(run)
    return manual_ids(st, step) or parse_ids(ids_from(path or step_report(run, step)))


def setids(run, step, raw):
    st = load(run)
    ids = parse_ids(raw)
    st.setdefault("manual", []).append({"step": step, "ids": ids, "raw": raw})
    save(run, st)
    print("manual ids", run, step, ids)


# ---------------------------------------------------------------- findings lists
def clean_body(lines):
    return [ln for ln in lines if not DROP_RE.match(ln)]


def findings_text(run, n):
    """Finding list for VF{n}, n >= 2 (n == 1 is written by merge)."""
    src = ws(run) / REVIEW / f"round{n}.md"
    text = src.read_text(errors="ignore")
    ids = step_ids(run, f"R{n}", src)
    prev = None
    for cand in (ws(run) / REVIEW / f"round{n-1}.orig.md", ws(run) / REVIEW / f"round{n-1}.md"):
        if n > 1 and cand.exists():
            prev = cand.read_text(errors="ignore")
            break
    parts = []
    for fid in ids:
        heading, body = sc.find_section(text, fid)
        if heading is None:
            hits = [ln for ln in text.splitlines() if re.search(rf"(?<![\w-]){re.escape(fid)}(?![\w-])", ln)][:10]
            parts.append(f"### {fid}\n" + "\n".join(hits))
            continue
        lines = [heading] + clean_body((body or "").splitlines())
        if not (body or "").strip() and n > 1 and prev is not None:
            h2, b2 = sc.find_section(prev, fid)
            if h2 is not None:
                lines += ["(text of this finding in the prior report)", h2] + clean_body((b2 or "").splitlines())
        parts.append(f"### {fid}\n" + "\n".join(lines))
    out = "\n\n".join(parts)
    (ws(run) / REVIEW / f"findings-{n}.md").write_text(out + "\n")
    return out, ids


def verify_brief_text(findings):
    rules = git_show(PRODUCT_REF, "src/superclaude/rules/prompts/document_review_loop_prompts.md")
    m = re.search(r'- Verify brief: "([^"]+)"', rules)
    assert m, "no Verify brief in the product rules file"
    return m.group(1).replace("{{CANDIDATE}}", SPEC).replace("{{FINDINGS}}", "\n\n" + findings + "\n")


def vf_sandbox(run, n):
    d = run_dir(run) / f"vf{n}"
    if d.exists():
        shutil.rmtree(d)
    (d / "ws" / REVIEW).mkdir(parents=True)
    (d / "home").mkdir(parents=True)
    (d / "ws" / SPEC).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(ws(run) / SPEC, d / "ws" / SPEC)
    return d


# ---------------------------------------------------------------- prep
def prep_audit(run, k):
    d = run_dir(run)
    ad = d / ("aud" if k == 1 else "aud2")
    if ad.exists():
        shutil.rmtree(ad)
    (ad / "home/.claude/rules/prompts").mkdir(parents=True)
    shutil.copytree(S1 / "inputs/repo-overlay", ad / "ws")
    (ad / "ws" / D / "review").mkdir(parents=True)
    shutil.copy(ws(run) / SPEC, ad / "ws" / SPEC)
    cmd = git_show(BASE_REF, "src/superclaude/commands/spec-panel.md")
    rules = (P11 / "rules.md").read_text()
    assert sha_text(cmd) == AUD_CMD_SHA, "frozen audit command hash mismatch"
    assert sha_text(rules) == AUD_RULES_SHA, "frozen audit rules hash mismatch"
    (ad / "command.md").write_text(cmd)
    (ad / "home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules)
    text = wrap(ad, audit_brief(), True)
    p = d / ("PROMPT-AUD.md" if k == 1 else "PROMPT-AUD2.md")
    p.write_text(text)
    return p


def mark_prepared(run, step):
    st = load(run)
    if step not in st["prepared"]:
        st["prepared"].append(step)
    save(run, st)


def prep(run, step, subs=None):
    subs = subs or {}
    d = run_dir(run)
    st = load(run)
    if step in ("AUD", "AUD2"):
        p = prep_audit(run, 1 if step == "AUD" else 2)
    elif step in R1S:
        x = step[-1].lower()
        sb = d / f"r1{x}"
        p = d / f"PROMPT-{step}.md"
        p.write_text(wrap(sb, brief_first(OUT[step]), True))
    elif step.startswith("VF"):
        n = int(step[2])
        if n == 1:
            findings = (ws(run) / REVIEW / "findings-1.md").read_text().rstrip("\n")
            ids = st["log"].get("VF1", {}).get("finding_ids") or [g["mid"] for g in st["merge"]["groups"]]
        else:
            findings, ids = findings_text(run, n)
        vf = vf_sandbox(run, n)
        b = verify_brief_text(findings) + f"\nWrite your full reply to {REVIEW}/verify-{n}.md. Do not edit anything else. Write only your output file."
        p = d / f"PROMPT-{step}.md"
        p.write_text(wrap(vf, b, False))
        st = load(run)
        st["log"].setdefault(step, {})["finding_ids"] = ids
        save(run, st)
    elif step in ("V1", "V2"):
        n = int(step[1])
        shutil.copy(ws(run) / SPEC, ws(run) / HIST / f"spec-v{n}.md")
        ids = subs.get("IDS") or ", ".join(st["log"][f"VF{n}"]["confirmed"])
        rep = f"{REVIEW}/round{n}.md"
        p = d / f"PROMPT-{step}.md"
        p.write_text(wrap(d, brief_revise(ids, rep, OUT[step]), False))
        print("IDS =", ids)
    elif step in ("R2", "R3"):
        n = int(step[1])
        prior = f"{REVIEW}/round{n-1}.md"
        base = f"{HIST}/spec-v{n-1}.md"
        p = d / f"PROMPT-{step}.md"
        p.write_text(wrap(d, brief_re(prior, base, OUT[step]), True))
    else:
        raise ValueError(step)
    mark_prepared(run, step)
    print(p)
    return p


# ---------------------------------------------------------------- merge
def merge(run):
    """Deterministic MERGE of the three first reviews. Returns the list of merged ids (empty if no blocking item)."""
    st = load(run)
    R = ws(run) / REVIEW
    items = []
    reviewers = {}
    for step in R1S:
        x = step[-1]
        p = R / f"round1-{x}.md"
        t = p.read_text(errors="ignore")
        v = sc.verdict_of(t)
        fs = blocking_findings(p, manual_ids(st, step))
        reviewers[x] = {"verdict": v, "sha256": sha(p), "ids": [f["id"] for f in fs], "themes": [f["theme"] for f in fs]}
        for f in fs:
            items.append(dict(f, src=f"round1-{x}.md"))
    spec_sha = sha(ws(run) / SPEC)
    head = ["review: 1 of 3", "", "# Merged first review (coordinator; MERGE rule over three independent first reviews)", "",
            f"candidate: {SPEC} sha256 {spec_sha}", "", "sources:"]
    srcs = [f"- {REVIEW}/round1-{x}.md verdict {reviewers[x]['verdict']} sha256 {reviewers[x]['sha256']}" for x in "abc"]
    if not items:
        (R / "round1.md").write_text("\n".join(head + srcs + ["", "No report has a blocking finding.", "", "verdict: PASS", ""]))
        st["merge"] = {"raw_count": 0, "merged_count": 0, "groups": [], "reviewers": reviewers, "done": True}
        st["loop_end"] = "PASS"
        save(run, st)
        return []
    parent = list(range(len(items)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if sc.same_defect(items[i], items[j]):
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[max(ri, rj)] = min(ri, rj)
    order, groups = {}, []
    for i in range(len(items)):
        r = find(i)
        if r not in order:
            order[r] = len(groups)
            groups.append([])
        groups[order[r]].append(i)
    lines = ["Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. "
             "Confirm Mn when any sub-entry holds, and name that sub-entry in the reason."]
    gl = []
    for gi, members in enumerate(groups, 1):
        mid = f"M{gi}"
        lines += ["", f"### {mid}"]
        gm = []
        for k, i in enumerate(members):
            it = items[i]
            letter = chr(ord("a") + k)
            lines += ["", f"#### {mid}.{letter} ({it['src']} {it['id']})", it["heading"] or f"(no section found for {it['id']})"]
            lines += clean_body((it["body"] or "").splitlines())
            gm.append(f"{it['src']}/{it['id']}")
        gl.append({"mid": mid, "theme": items[members[0]]["theme"], "members": gm,
                   "cited": sorted(set().union(*[items[i]["cited"] for i in members])),
                   "heading": items[members[0]]["heading"]})
    (R / "findings-1.md").write_text("\n".join(lines) + "\n")
    st["merge"] = {"raw_count": len(items), "merged_count": len(groups), "groups": gl, "reviewers": reviewers, "done": True}
    st.setdefault("log", {}).setdefault("VF1", {})["finding_ids"] = [g["mid"] for g in gl]
    save(run, st)
    return [g["mid"] for g in gl]


def strip_heading(h):
    return re.sub(r"^\s*(?:#+\s*)?(?:[-*]\s*)?(?:\*\*)?", "", h or "").strip()


def member_section(run, member):
    src, fid = member.split("/", 1)
    t = (ws(run) / REVIEW / src).read_text(errors="ignore")
    h, b = sc.find_section(t, fid)
    return src, fid, h, b


def parse_verify(text, ids):
    """-> ({id: (verdict, reason)}, parse_ok). Fails closed (confirm) when nothing parses."""
    lines = text.splitlines()
    conf_lines = [ln for ln in lines if re.match(r"(?i)^\W*confirmed:", ln)]
    res = {}
    for fid in ids:
        tok = re.compile(rf"(?<![\w-]){re.escape(fid)}(?![\w-])")
        lead = re.compile(rf"^\W*(?:\*\*)?{re.escape(fid)}(?![\w-])")  # row must START with the id (fix 2026-11-10: another row's reason text mentioning the id was matched first)
        hit = next((ln for ln in lines if lead.search(ln) and re.search(r"(?i)\b(confirm|reject)", ln)
                    and not re.match(r"(?i)^\W*confirmed:", ln)), None)
        if hit is None:
            hit = next((ln for ln in lines if tok.search(ln) and re.search(r"(?i)\b(confirm|reject)", ln)
                        and not re.match(r"(?i)^\W*confirmed:", ln)), None)
        if hit is not None:
            cells = [c.strip() for c in hit.split("|") if c.strip()]
            vc = [c.lower() for c in cells[1:-1] if c.lower() in ("confirm", "reject", "confirmed", "rejected")]  # verdict cell wins over words in the reason text (fix 2026-11-10)
            if vc:
                verdict = "reject" if vc[-1].startswith("reject") else "confirm"
            else:
                verdict = "reject" if re.search(r"(?i)\breject", hit) else "confirm"
            reason = cells[-1] if len(cells) > 1 else hit.strip()
            res[fid] = (verdict, reason)
    if len(res) == len(ids) and ids:
        return res, True
    if conf_lines:
        m = re.search(r"(?im)^\W*confirmed:\s*(.*)$", "\n".join(conf_lines[-1:]))
        listed = set(parse_ids(m.group(1))) if m else set()
        for fid in ids:
            if fid not in res:
                res[fid] = ("confirm", "listed in confirmed line") if fid in listed else ("reject", "not in confirmed line")
        return res, True
    if res:
        for fid in ids:
            res.setdefault(fid, ("confirm", "no verdict parsed"))
        return res, False
    return {fid: ("confirm", "no verdict parsed (fail closed)") for fid in ids}, False


def noted(run, st, step, fid, theme, cited, heading, reason):
    st["noted_unactioned"].append({"step": step, "id": fid, "theme": theme, "cited": sorted(cited), "heading": heading, "reason": reason})
    nf = run_dir(run) / "NOTED.md"
    if not nf.exists():
        nf.write_text("| step | id | theme | verifier reason |\n|---|---|---|---|\n")
    with open(nf, "a") as f:
        f.write(f"| {step} | {fid} | {theme} | {reason.replace('|', '/')} |\n")


def ingest_vf(run, st, n, outp):
    text = outp.read_text(errors="ignore")
    R = ws(run) / REVIEW
    ids = st["log"].get(f"VF{n}", {}).get("finding_ids") or []
    table, ok = parse_verify(text, ids)
    print(f"  verify table {run} VF{n} parse_ok={ok}")
    for fid in ids:
        print(f"   {fid}: {table[fid][0]} ({table[fid][1][:100]})")
    confirmed = [i for i in ids if table[i][0] == "confirm"]
    rejected = {i: table[i][1] for i in ids if table[i][0] == "reject"}
    shutil.copy(outp, R / f"verify-{n}.md")
    c_txt = ", ".join(confirmed) or "none"
    r_txt = "; ".join(f"{i} (verifier: {r})" for i, r in rejected.items()) or "none"
    block = VERIFY_BLOCK.format(n=n, c=c_txt, r=r_txt)
    meta = {}
    if n == 1:
        gl = {g["mid"]: g for g in st["merge"]["groups"]}
        for fid, reason in rejected.items():
            g = gl[fid]
            noted(run, st, "VF1", fid, g["theme"], g["cited"], g["heading"], reason)

        def render(mid):
            out = [f"### {mid}" if mid in confirmed else f"### {mid} (verifier: {rejected.get(mid, '')})"]
            for k, m in enumerate(gl[mid]["members"]):
                src, fid, h, b = member_section(run, m)
                out += ["", f"#### {mid}.{chr(97 + k)}, from {src} {fid}: {strip_heading(h)}", b or ""]
            return out
        rep = ["review: 1 of 3", "", "# Merged first review (coordinator; MERGE rule over three independent first reviews)", "",
               f"candidate: {SPEC} sha256 {sha(ws(run) / SPEC)}", "", "sources:"]
        rep += [f"- {REVIEW}/round1-{x}.md verdict {st['merge']['reviewers'][x]['verdict']} sha256 {st['merge']['reviewers'][x]['sha256']}" for x in "abc"]
        rep += ["", block, "", "## Blocking findings (merged, confirmed)", ""]
        for mid in confirmed:
            rep += render(mid) + [""]
        if not confirmed:
            rep += ["None.", ""]
        rep += ["## Noted, unactioned (verifier rejected; not prior blocking findings)", ""]
        for mid in rejected:
            rep += render(mid) + [""]
        if not rejected:
            rep += ["None.", ""]
        rep += ["## Follow-up candidates", "", "Listed in the three source reports above; not merged.", "", "## Reviser brief", "",
                (f"Blocking finding ids: {', '.join(confirmed)}." if confirmed else "Blocking finding ids: none (no merged finding was confirmed)."),
                REVISER_RULES, "", "verdict: FAIL", ""]
        (R / "round1.md").write_text("\n".join(rep))
    else:
        rp = R / f"round{n}.md"
        orig = R / f"round{n}.orig.md"
        if not orig.exists():
            shutil.copy(rp, orig)
        lines = orig.read_text(errors="ignore").splitlines()
        at = next((i for i, ln in enumerate(lines) if re.match(r"^\W*review:\s*\d\s*of\s*3", ln, re.I)), None)
        lines.insert(0 if at is None else at + 1, block)
        rp.write_text("\n".join(lines) + "\n")
        src = orig.read_text(errors="ignore")
        for fid, reason in rejected.items():
            h, b = sc.find_section(src, fid)
            noted(run, st, f"VF{n}", fid, sc.tag(h, b), sc.cited((h or "") + "\n" + (b or "")), h, reason)
    meta = {"finding_ids": ids, "confirmed": confirmed, "rejected": rejected, "parse_ok": ok}
    return meta


# ---------------------------------------------------------------- ingest
def out_path(run, step):
    d = run_dir(run)
    if step in R1S:
        return d / f"r1{step[-1].lower()}" / "ws" / OUT[step]
    if step.startswith("VF"):
        return d / f"vf{step[2]}" / "ws" / OUT[step]
    if step == "AUD":
        return d / "aud" / "ws" / AUD_OUT
    if step == "AUD2":
        return d / "aud2" / "ws" / AUD_OUT
    return ws(run) / OUT[step]


def ingest(run, step):
    st = load(run)
    outp = out_path(run, step)
    rec = {"output_exists": outp.exists()}
    old = st["log"].get(step, {})
    for k in ("output_tokens", "finding_ids"):
        if k in old:
            rec[k] = old[k]
    if outp.exists():
        t = outp.read_text(errors="ignore")
        rec["report_bytes"] = len(t.encode())
        if step in R1S + ["R2", "R3", "AUD", "AUD2"]:
            rec["verdict"] = sc.verdict_of(t)
            rec["review_header"] = re.findall(r"^\W*review:\s*(\d)\s*of\s*3", t, re.I | re.M)
            rec["labels"] = dict(collections.Counter(re.findall(r"\b(CRITICAL|MAJOR|MINOR)\b", t)))
            rec["blocking_ids"] = ids_from(outp)
            rec["blocking_word_count"] = len(re.findall(r"blocking", t, re.I))
        if step in R1S:
            shutil.copy(outp, ws(run) / REVIEW / f"round1-{step[-1].lower()}.md")
        if step.startswith("VF"):
            rec.update(ingest_vf(run, st, int(step[2]), outp))
    if step in ("AUD", "AUD2"):
        base = outp.parents[len(pathlib.PurePosixPath(AUD_OUT).parts) - 1]
        rec["spec_audited"] = {"bytes": (base / SPEC).stat().st_size if (base / SPEC).exists() else None}
    elif step not in R1S and not step.startswith("VF"):
        rec["spec_after"] = spec_stats(ws(run))
    st["log"][step] = rec
    if step not in st["done"]:
        st["done"].append(step)
    save(run, st)
    print(json.dumps({run: {step: {k: v for k, v in rec.items() if k not in ("labels",)}}}, indent=1))
    return rec


def unlaunch(run, step, quiet=False):
    """Drop a ledger entry. Second call for the same step marks the run lost."""
    st = load(run)
    st["launched"].pop(step, None)
    if step in st["done"]:
        st["done"].remove(step)
    if step in st["transitioned"]:
        st["transitioned"].remove(step)
    st["log"].pop(step, None)
    n = st["relaunch"].get(step, 0) + 1
    st["relaunch"][step] = n
    outp = out_path(run, step)
    if outp.exists():
        outp.rename(outp.with_name(outp.name + f".failed{n}"))
    if step in ("V1", "V2"):
        snap = ws(run) / HIST / f"spec-v{step[1]}.md"
        if snap.exists():
            shutil.copy(snap, ws(run) / SPEC)
    if n > 1:
        st["lost"] = True
    save(run, st)
    if not quiet:
        print(("LOST " if n > 1 else "unlaunched ") + f"{run} {step}")
    return n


# ---------------------------------------------------------------- transcripts / tokens
def first_user_text(lines):
    for ln in lines[:12]:
        try:
            d = json.loads(ln)
        except Exception:
            continue
        m = d.get("message") or {}
        if d.get("type") == "user" and m.get("role") == "user":
            c = m.get("content")
            if isinstance(c, list):
                return " ".join(x.get("text", "") for x in c if isinstance(x, dict))
            return c if isinstance(c, str) else ""
    return ""


def transcript_info(path):
    try:
        lines = pathlib.Path(path).read_text(errors="ignore").splitlines()
    except Exception:
        return None
    first = first_user_text(lines)
    ids, models, done, last_text = {}, collections.Counter(), False, ""
    anon = 0
    for ln in lines:
        try:
            d = json.loads(ln)
        except Exception:
            continue
        m = d.get("message") or {}
        if m.get("role") != "assistant":
            continue
        mid = m.get("id")
        if mid is None:
            anon += 1
            mid = f"anon{anon}"
        ot = (m.get("usage") or {}).get("output_tokens") or 0
        ids[mid] = max(ids.get(mid, 0), ot)
        if m.get("model"):
            models[m["model"]] += 1
        if isinstance(m.get("content"), list):
            for c in m["content"]:
                if isinstance(c, dict):
                    if c.get("type") == "tool_use" and c.get("name") == "SubagentHandback" and "DONE" in json.dumps(c.get("input")):
                        done = True
                    if c.get("type") == "text":
                        last_text = c.get("text", "")
    if "DONE" in last_text:
        done = True
    return {"path": str(path), "first": first, "model": models.most_common(1)[0][0] if models else "", "tokens": sum(ids.values()), "done": done}


def scan_transcripts(pattern_re, tasks_glob=None):
    """-> {(run, step): [info,...]} for transcripts whose (short) first user message names a PROMPT file."""
    import glob
    out = collections.defaultdict(list)
    for f in sorted(glob.glob(tasks_glob or TASKS_GLOB)):
        info = transcript_info(f)
        if not info or len(info["first"]) > 3000:
            continue
        m = re.search(pattern_re, info["first"])
        if m:
            out[(m.group(1), m.group(2))].append(info)
    return out


NEW_PAT = r"p12/ab1/runs/(b1h?-r\d+)/PROMPT-(\w+)\.md"
OLD_PAT = r"p11/runs/(a3-r\d)/PROMPT-(\w+)\.md"


def pick(cands, expected, label=""):
    """Apply rule 5: keep expected-model transcripts; prefer DONE + most tokens."""
    keep = []
    for c in cands:
        if expected in c["model"]:
            keep.append(c)
        else:
            print(f"WARN {label}: transcript {pathlib.Path(c['path']).name} model {c['model']!r} is not {expected}; ignored")
    if not keep:
        return None
    if len(keep) > 1:
        print(f"WARN {label}: {len(keep)} transcripts remain; keeping the DONE one with most tokens")
    keep.sort(key=lambda c: (c["done"], c["tokens"]), reverse=True)
    return keep[0]


def expected_model(st, step):
    return "sonnet" if step in ("AUD", "AUD2") else st["loop_model"]


def tokens_cmd(only_run=None):
    idx = scan_transcripts(NEW_PAT)
    for run in all_runs():
        if only_run and run != only_run:
            continue
        st = load(run)
        for step in STEPS:
            c = idx.get((run, step))
            if not c:
                continue
            best = pick(c, expected_model(st, step), f"{run} {step}")
            if best and step in st["log"]:
                st["log"][step]["output_tokens"] = best["tokens"]
        save(run, st)
        loop = sum(st["log"].get(s, {}).get("output_tokens", 0) for s in LOOP_STEPS)
        print(run, "loop", loop, "aud", st["log"].get("AUD", {}).get("output_tokens"), "aud2", st["log"].get("AUD2", {}).get("output_tokens"))


def basetokens():
    idx = scan_transcripts(OLD_PAT)
    loops, auds = [], []
    for r in range(1, 7):
        run = f"a3-r{r}"
        tot = {}
        for (rn, step), c in idx.items():
            if rn == run:
                best = pick(c, "sonnet", f"{run} {step}")
                if best:
                    tot[step] = best["tokens"]
        loop = sum(v for k, v in tot.items() if k != "AUD")
        loops.append(loop)
        auds.append(tot.get("AUD", 0))
        print(run, "loop", loop, "audit", tot.get("AUD"), dict(sorted(tot.items())))
    ml, ma = sum(loops) / len(loops), sum(auds) / len(auds)
    print(f"loop mean {ml:,.0f} (expected 100,424)  audit mean {ma:,.0f} (expected 69,044)")
    return ml, ma


# ---------------------------------------------------------------- status
def status():
    for run in all_runs():
        st = load(run)
        row = []
        for s in STEPS:
            r = st["log"].get(s)
            row.append(f"{s}:-" if r is None else f"{s}:{r.get('verdict', 'ok' if r['output_exists'] else 'MISSING')}")
        flag = "LOST" if st["lost"] else ("complete" if st["complete"] else "")
        print(run, st["stratum"], " ".join(row), "| loop_end", st["loop_end"], flag)


# ---------------------------------------------------------------- analysis (post-hoc; D2 loop-only cost, D6 no mid-run cost checks)
def frac(x): return Fraction(x[0], x[1])


def overrides():
    p = AB / "theme-overrides.json"
    return json.load(open(p)) if p.exists() else {}


def score_report(path, key, ids=None, ov=None, used=None):
    fs = blocking_findings(path, ids)
    ov = overrides() if ov is None else ov
    for f in fs:
        k = f"{key}/{f['id']}"
        if k in ov:
            f["theme"] = ov[k]
            if used is not None:
                used.append(k)
    return fs


def themes_hit(fs): return {f["theme"] for f in fs if f["theme"] in ("T1", "T2", "T3")}


def run_record(run, ov=None, used=None):
    st = load(run)
    log = st["log"]
    rec = {"run": run, "stratum": st["stratum"], "lost": st["lost"], "complete": st["complete"], "loop_end": st["loop_end"],
           "relaunched": sum(st["relaunch"].values()) > 0 or bool(st["lost"]), "manual": len(st["manual"])}
    rec["rounds"] = 1 + ("R2" in log) + ("R3" in log) if any(r in log for r in R1S) else 0
    rec["agents"] = sum(1 for s in ("R1a", "R1b", "R1c", "R2", "R3") if s in log)
    rec["loop_tokens"] = sum(log.get(s, {}).get("output_tokens", 0) for s in LOOP_STEPS)
    rec["aud_tokens"] = [log.get(s, {}).get("output_tokens") for s in ("AUD", "AUD2")]
    rec["tokens_missing"] = [s for s in LOOP_STEPS if s in log and "output_tokens" not in log[s]]
    fin = st.get("final_spec") or {}
    rec["final_bytes"] = fin.get("bytes")
    rec["audits"] = []
    for step, key in (("AUD", "audit.md"), ("AUD2", "audit2.md")):
        p = out_path(run, step)
        if p.exists() and log.get(step, {}).get("verdict") in ("PASS", "FAIL"):
            fs = score_report(p, f"{run}/{key}", manual_ids(st, step), ov, used)
            rec["audits"].append({"step": step, "verdict": log[step]["verdict"], "findings": fs})
    rec["reviewers"] = {}
    for x in "abc":
        p = ws(run) / REVIEW / f"round1-{x}.md"
        if p.exists():
            fs = score_report(p, f"{run}/round1-{x}.md", manual_ids(st, f"R1{x}"), ov, used)
            rec["reviewers"][x] = {"verdict": sc.verdict_of(p.read_text(errors="ignore")), "findings": fs}
    rec["merge"] = {k: st["merge"].get(k) for k in ("raw_count", "merged_count")}
    rec["vf"] = {s: {k: log[s].get(k) for k in ("finding_ids", "confirmed", "rejected", "parse_ok")} for s in ("VF1", "VF2", "VF3") if s in log}
    rec["noted"] = st["noted_unactioned"]
    return rec


def baseline_values(dec):
    """B_* over all baseline audits that exist. -> (values dict, provisional bool, notes list)."""
    notes, scores = [], []
    for r in range(1, 7):
        p = P11 / "runs" / f"a3-r{r}" / "aud/ws" / AUD_OUT
        if p.exists():
            t = p.read_text(errors="ignore")
            if sc.verdict_of(t) in ("PASS", "FAIL"):
                scores.append((sc.verdict_of(t), blocking_findings(p)))
    a2dir = pathlib.Path(dec["baseline_audit2_path"])
    n2 = 0
    for r in range(1, 7):
        p = a2dir / f"a3-r{r}/ws" / AUD_OUT
        if p.exists():
            t = p.read_text(errors="ignore")
            if sc.verdict_of(t) in ("PASS", "FAIL"):
                scores.append((sc.verdict_of(t), blocking_findings(p)))
                n2 += 1
            else:
                notes.append(f"baseline second audit a3-r{r} is {sc.verdict_of(t)}; excluded")
        else:
            notes.append(f"baseline second audit a3-r{r} missing")
    d0 = dec["B_DEFAULT"]
    if n2 == 0:
        return {"B_BLK": d0["B_BLK"], "B_AUDFAIL": frac(d0["B_AUDFAIL"]), "B_THEME": frac(d0["B_THEME"]), "B_GROWTH": d0["B_GROWTH"],
                "n_audits": 6}, True, notes + ["no baseline second audit: PROVISIONAL (single baseline audit)"]
    n = len(scores)
    return {"B_BLK": sum(len(f) for _, f in scores) / n,
            "B_AUDFAIL": Fraction(sum(v == "FAIL" for v, _ in scores), n),
            "B_THEME": Fraction(sum(bool(themes_hit(f)) for _, f in scores), n),
            "B_GROWTH": d0["B_GROWTH"], "n_audits": n}, False, notes


def decide(recs, dec, base, n_expected, audit_idx=None):
    """Pre-registered rules of section 3 on completed Sonnet runs. audit_idx None = pooled, 0/1 = one replica only.
    Cost (R_LOOP) enters only here, after the runs exist (D6)."""
    rules = dec["rules"]
    done = [r for r in recs if r["complete"] and not r["lost"]]
    out = {"n_completed": len(done), "n_expected": n_expected}
    aud = [a for r in done for i, a in enumerate(r["audits"]) if audit_idx is None or i == audit_idx]
    out["n_audits"] = len(aud)
    out["BLK_T"] = sum(len(a["findings"]) for a in aud) / len(aud) if aud else None
    out["audit_fail"] = sum(a["verdict"] == "FAIL" for a in aud)
    out["theme_rate"] = sum(bool(themes_hit(a["findings"])) for a in aud)
    out["theme_counts"] = {t: sum(any(f["theme"] == t for f in a["findings"]) for a in aud) for t in ("T1", "T2", "T3", "other")}
    out["loop_pass"] = sum(r["loop_end"] in ("PASS", "VERIFIED-PASS") for r in done)
    out["growth"] = (sum((r["final_bytes"] - dec["SPEC_BYTES"]) / dec["SPEC_BYTES"] for r in done if r["final_bytes"]) / len(done)) if done else None
    out["LOOP_T"] = sum(r["loop_tokens"] for r in done) / len(done) if done else None
    out["TOK_T"] = (out["LOOP_T"] + sum(t for r in done for t in r["aud_tokens"][:1] if t) / len(done)) if done else None
    out["R_LOOP"] = out["LOOP_T"] / dec["A_BASE"] if done else None     # decides
    out["R_B"] = out["TOK_T"] / dec["B_BASE"] if done else None        # reported only
    n1 = sum(len(r["vf"].get("VF1", {}).get("finding_ids") or []) for r in done)
    j1 = sum(len(r["vf"].get("VF1", {}).get("rejected") or {}) for r in done)
    out["REJ1"], out["N1"] = j1, n1
    out["REJ1_rate"] = j1 / n1 if n1 else None
    key = str(n_expected)
    reasons = []
    if len(done) < dec["MIN_COMPLETED"][key]:
        out["outcome"] = "INCONCLUSIVE"
        out["rule"] = f"fewer than {dec['MIN_COMPLETED'][key]} completed runs"
        return out
    B = base
    if out["BLK_T"] > rules["DROP1_BLK_FACTOR"] * B["B_BLK"]:
        reasons.append(("DROP", "DROP-1 no recall gain"))
    elif out["R_LOOP"] > rules["DROP2_RLOOP_LIMIT"] and out["BLK_T"] > rules["DROP2_BLK_FACTOR"] * B["B_BLK"]:
        reasons.append(("DROP", "DROP-2 cost without gain"))
    elif out["REJ1_rate"] is not None and out["REJ1_rate"] > rules["DROP3_REJ_RATE"]:
        reasons.append(("DROP", "DROP-3 verifier rejected more than half of merged findings"))
    elif out["loop_pass"] < rules["DROP4_PASS_MIN"][key] or out["growth"] > rules["DROP4_GROWTH_FACTOR"] * B["B_GROWTH"]:
        reasons.append(("DROP", "DROP-4 harm"))
    else:
        limit = int(Fraction(str(rules["ADOPT_AUDFAIL_FACTOR"])) * B["B_AUDFAIL"] * len(aud))
        if (out["BLK_T"] <= rules["ADOPT_BLK_FACTOR"] * B["B_BLK"] and out["audit_fail"] <= limit
                and out["growth"] <= rules["ADOPT_GROWTH_FACTOR"] * B["B_GROWTH"]):
            reasons.append(("ADOPT", "ADOPT"))
        else:
            reasons.append(("INCONCLUSIVE", "no DROP and not a clear ADOPT"))
    out["outcome"], out["rule"] = reasons[0]
    return out


def haiku_baseline(dec):
    """-> {H_BLK, H_LOOP, fail_rate, notes} from the shared Haiku baseline, or None if absent."""
    p = pathlib.Path(dec["haiku"]["baseline_path"])
    if not p.exists():
        return None
    j = json.load(open(p))
    notes = []
    runs = j.get("runs", j) if isinstance(j, dict) else {}
    rows = list(runs.values()) if isinstance(runs, dict) else list(runs)
    rows = [r for r in rows if isinstance(r, dict)]
    h_blk = j.get("H_BLK") if isinstance(j, dict) else None
    h_loop = j.get("H_LOOP") if isinstance(j, dict) else None
    if h_blk is None:
        vals = []
        for r in rows:
            v = r.get("blocking_per_audit") or r.get("blocking_counts") or r.get("n_blocking")
            if isinstance(v, list):
                vals += v
            elif isinstance(v, (int, float)):
                vals.append(v)
        h_blk = sum(vals) / len(vals) if vals else None
        if h_blk is None:
            notes.append("results.json has no recognisable blocking counts")
    if h_loop is None:
        vals = [r.get("loop_tokens") or r.get("loop") for r in rows if isinstance(r.get("loop_tokens") or r.get("loop"), (int, float))]
        h_loop = sum(vals) / len(vals) if vals else None
    fail = j.get("harness_failure_rate") if isinstance(j, dict) else None
    if fail is None:
        fail = sum(bool(r.get("lost") or r.get("manual")) for r in rows) / len(rows) if rows else 0.0
    notes.append("Haiku baseline audit reports were not rescored here (format of results.json unverified at build time)")
    return {"H_BLK": h_blk, "H_LOOP": h_loop, "fail_rate": fail, "notes": notes}


def haiku_stratum(recs_h, hb, dec):
    if not recs_h or hb is None or hb.get("H_BLK") in (None, 0):
        return {"state": "pending"}
    settled = [r for r in recs_h if r["complete"] or r["lost"]]
    if len(settled) < dec["N_HAIKU"]:
        return {"state": "pending"}
    done = [r for r in recs_h if r["complete"] and not r["lost"]]
    aud = [a for r in done for a in r["audits"]]
    blk = sum(len(a["findings"]) for a in aud) / len(aud) if aud else None
    fail_rate = sum(r["relaunched"] for r in recs_h) / len(recs_h)
    hr = blk / hb["H_BLK"] if blk is not None else None
    ok = hr is not None and (1 - hr) > 0 and fail_rate <= hb["fail_rate"] + dec["haiku"]["harness_fail_margin"]
    loop = sum(r["loop_tokens"] for r in done) / len(done) if done else None
    return {"state": "ok" if ok else "disagrees", "BLK_TH": blk, "H_BLK": hb["H_BLK"], "HR": hr, "one_minus_HR": None if hr is None else 1 - hr,
            "fail_rate": fail_rate, "H_fail_rate": hb["fail_rate"], "loop_pass": sum(r["loop_end"] in ("PASS", "VERIFIED-PASS") for r in done),
            "n_done": len(done), "growth": (sum((r["final_bytes"] - dec["SPEC_BYTES"]) / dec["SPEC_BYTES"] for r in done if r["final_bytes"]) / len(done)) if done else None,
            "R_LOOP_H": (loop / hb["H_LOOP"]) if loop and hb.get("H_LOOP") else None}


def final_outcome(sonnet, replicas, hk):
    """Replica agreement, then the Haiku condition. Returns (outcome, eligible_for_extension, note)."""
    o = sonnet["outcome"]
    if len({r["outcome"] for r in replicas}) > 1:
        return "INCONCLUSIVE", True, "the two audit replicas disagree"
    if o == "ADOPT":
        if hk["state"] == "pending":
            return "ADOPT (Haiku robustness pending)", False, "Haiku stratum or baseline missing"
        if hk["state"] == "disagrees":
            return "INCONCLUSIVE", False, "Haiku stratum disagrees"
        return "ADOPT", False, ""
    return o, o == "INCONCLUSIVE", ""


def design_tables(recs):
    """Design-specific metrics (Part E)."""
    lines = []
    cap = {t: 0 for t in ("T1", "T2", "T3")}
    ns = 0
    for r in recs:
        for x, v in r["reviewers"].items():
            ns += 1
            for t in themes_hit(v["findings"]):
                cap[t] += 1
    lines += ["### Per-theme capture across the reviewers (pooled first-review samples)", "",
              "| theme | captured / samples | baseline k=1 |", "|---|---|---|"]
    for t, b in (("T1", "6/6"), ("T2", "2/6"), ("T3", "3/6")):
        lines.append(f"| {t} | {cap[t]}/{ns} | {b} |")
    lines += ["", "| run | a | b | c | union |", "|---|---|---|---|---|"]
    k1s, k2s, k3s, adds = [], [], [], 0
    for r in recs:
        th = {x: themes_hit(v["findings"]) for x, v in r["reviewers"].items()}
        U = set().union(*th.values()) if th else set()
        cells = [f"{v['verdict']} {len(v['findings'])} {','.join(sorted(th[x])) or '-'}" for x, v in sorted(r["reviewers"].items())]
        lines.append(f"| {r['run']} | " + " | ".join(cells) + f" | {','.join(sorted(U)) or '-'} |")
        if U and len(th) == 3:
            xs = list(th)
            k1s.append(sum(len(th[x] & U) / len(U) for x in xs) / 3)
            pairs = [(xs[0], xs[1]), (xs[0], xs[2]), (xs[1], xs[2])]
            k2s.append(sum(len((th[a] | th[b]) & U) / len(U) for a, b in pairs) / 3)
            k3s.append(1.0)
            adds += sum((th[a] | th[b]) != U for a, b in pairs)
    if k1s:
        m = lambda v: sum(v) / len(v)  # noqa: E731
        lines += ["", f"k=1 capture {m(k1s):.2f}; k=2 capture {m(k2s):.2f}; k=3 capture 1.00; pairs whose third reviewer adds a theme: {adds}"
                  + (" (k=2 would likely suffice)" if m(k2s) >= 0.9 else "")]
    lines += ["", "### Merged-finding count", "", "| run | raw | merged | dedup ratio |", "|---|---|---|---|"]
    for r in recs:
        raw, mg = r["merge"].get("raw_count"), r["merge"].get("merged_count")
        lines.append(f"| {r['run']} | {raw} | {mg} | {(mg / raw if raw else 0):.2f} |")
    lines += ["", "### Verifier", "", "| run | step | sent | confirmed | rejected | parse_ok |", "|---|---|---|---|---|---|"]
    ts = tj = 0
    for r in recs:
        for s, v in r["vf"].items():
            sent = len(v.get("finding_ids") or [])
            rj = len(v.get("rejected") or {})
            ts += sent
            tj += rj
            lines.append(f"| {r['run']} | {s} | {sent} | {len(v.get('confirmed') or [])} | {rj} | {v.get('parse_ok')} |")
    lines.append(f"\npooled rejection rate over all VF steps: {tj}/{ts}")
    lines += ["", "### Noted, unactioned vs audits", "", "| run | step | id | theme | verifier reason | matched audit blocker | eyeball |", "|---|---|---|---|---|---|---|"]
    for r in recs:
        for n in r["noted"]:
            f = {"theme": n["theme"], "cited": set(n["cited"])}
            hit = [f"{a['step']}/{g['id']}" for a in r["audits"] for g in a["findings"] if sc.matches_audit(f, g)]
            lines.append(f"| {r['run']} | {n['step']} | {n['id']} | {n['theme']} | {n['reason'][:80]} | {', '.join(hit) or 'none'} | (eyeball) |")
    return "\n".join(lines)


def analyze():
    dec = decision()
    base, prov, bnotes = baseline_values(dec)
    used, eyeball = [], []
    recs = {"sonnet": [], "haiku": []}
    for run in all_runs():
        r = run_record(run, None, used)
        recs[r["stratum"]].append(r)
        for a in r["audits"] + [{"step": f"R1{x}", "findings": v["findings"]} for x, v in r["reviewers"].items()]:
            for f in a["findings"]:
                eyeball.append(f"{run} {a['step']} {f['id']} {f['theme']} :: {(f['heading'] or '')[:100]}")
    S6 = recs["sonnet"]
    n_exp = decision()["N_SONNET"] + (decision()["N_EXTEND"] if any(r["run"] == f"b1-r{decision()['N_SONNET'] + 1}" for r in S6) else 0)
    sonnet = decide(S6, dec, base, n_exp)
    replicas = [decide(S6, dec, base, n_exp, i) for i in (0, 1)]
    hb = haiku_baseline(dec)
    hk = haiku_stratum(recs["haiku"], hb, dec)
    outcome, eligible, note = final_outcome(sonnet, replicas, hk)
    metrics = {"sonnet": dict(sonnet, outcome_final=outcome, n_runs=n_exp, extension_eligible=eligible and n_exp == decision()["N_SONNET"], note=note,
                               replicas=[{k: r[k] for k in ("outcome", "BLK_T", "rule")} for r in replicas]),
               "haiku": hk, "baseline": {k: (float(v) if isinstance(v, Fraction) else v) for k, v in base.items()},
               "provisional": prov, "stratum": "sonnet"}
    json.dump(metrics, open(AB / "metrics.json", "w"), indent=1, default=str)
    T = []
    tag_ = "PROVISIONAL " if prov else ""
    T.append(f"# ab1 tables ({tag_}n={n_exp})\n")
    T.append(f"Outcome: **{outcome}** ({sonnet['rule']}){' - ' + note if note else ''}; R_LOOP {sonnet['R_LOOP']} (decides, limit {dec['rules']['DROP2_RLOOP_LIMIT']}), R_B {sonnet['R_B']} (reported only)\n")
    T.append(f"Baseline: B_BLK {base['B_BLK']:.2f}, B_AUDFAIL {float(base['B_AUDFAIL']):.3f}, B_THEME {float(base['B_THEME']):.3f} over {base['n_audits']} audits; " + "; ".join(bnotes) + "\n")
    T.append("## Sonnet stratum\n\n| run | loop end | rounds / agents | growth | LOOP | AUD tokens | audit 1 | audit 2 |\n|---|---|---|---|---|---|---|---|")
    for r in S6:
        au = [f"{a['verdict']} " + ",".join(f"{g['id']}:{g['theme']}" for g in a["findings"]) for a in r["audits"]]
        gr = f"{(r['final_bytes'] - dec['SPEC_BYTES']) / dec['SPEC_BYTES']:+.2%}" if r["final_bytes"] else "-"
        T.append(f"| {r['run']}{' LOST' if r['lost'] else ''} | {r['loop_end']} | {r['rounds']} / {r['agents']} | {gr} | {r['loop_tokens']} | {r['aud_tokens']} | {au[0] if au else '-'} | {au[1] if len(au) > 1 else '-'} |")
    T.append("\n## Metrics (pooled over completed audits; replicas below)\n")
    for k in ("n_completed", "n_audits", "BLK_T", "audit_fail", "theme_rate", "theme_counts", "loop_pass", "growth", "LOOP_T", "TOK_T", "R_LOOP", "R_B", "REJ1", "N1", "REJ1_rate"):
        T.append(f"- {k}: {sonnet.get(k)}")
    for i, r in enumerate(replicas, 1):
        T.append(f"- replica audit {i} only: {r['outcome']} (BLK_T {r['BLK_T']}, {r['rule']})")
    T.append("\n## Haiku stratum (never pooled)\n")
    T.append(json.dumps(hk, indent=1, default=str))
    T.append("\n## Design-specific tables (Sonnet)\n")
    T.append(design_tables(S6))
    T.append("\n## Theme tags to eyeball\n\n" + "\n".join(f"- {e}" for e in eyeball))
    T.append("\n## Theme overrides applied\n\n" + ("\n".join(f"- {u}" for u in sorted(set(used))) or "none"))
    ab2 = pathlib.Path(dec["ab2_metrics_path"])
    T.append("\n## b1 vs b2 (k ablation)\n\n" + ("ab2 metrics.json present: compare by hand (schema not fixed): " + str(ab2) if ab2.exists() else "ablation pending (no ab2 metrics.json)"))
    (AB / "RESULTS-tables.md").write_text("\n".join(T) + "\n")
    print("\n".join(T[:6]))
    return metrics


def main(argv):
    c = argv[1]
    if c == "build":
        st = "haiku" if "--stratum" in argv and argv[argv.index("--stratum") + 1] == "haiku" else "sonnet"
        build(st, "--extend" in argv)
    elif c == "prep":
        prep(argv[2], argv[3], dict(kv.split("=", 1) for kv in argv[4:]))
    elif c == "ingest":
        ingest(argv[2], argv[3])
    elif c == "setids":
        setids(argv[2], argv[3], argv[4])
    elif c == "unlaunch":
        unlaunch(argv[2], argv[3])
    elif c == "status":
        status()
    elif c == "tokens":
        tokens_cmd(argv[2] if len(argv) > 2 else None)
    elif c == "basetokens":
        basetokens()
    elif c == "analyze":
        analyze()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
