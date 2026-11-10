#!/usr/bin/env python3
"""A/B design 2 harness: verify-before-fix gate (k=1) in the spec-panel review loop.  Usage:
  harness.py build [--stratum sonnet|haiku] [--extend]   create sandboxes (b2-r1..r6 | b2h-r1..r4 | b2-r7..r9)
  harness.py prep RUN STEP [K=V ...]   write RUN/PROMPT-STEP.md (STEP in R1 VF1 V1 R2 VF2 V2 R3 VF3 AUD AUD2)
  harness.py ingest RUN STEP           record outputs of a finished step
  harness.py setids RUN STEP "F1, F2"  manual blocking ids for a FAIL review whose ids could not be parsed
  harness.py unlaunch RUN STEP         drop a launch-ledger entry and re-queue the step (second time: run lost)
  harness.py tokens                    attach deduplicated output tokens from the worker transcripts to every step
  harness.py basetokens                recompute the Stage 2 arm-3 token totals (must match plan section 2)
  harness.py status                    table of all runs
  harness.py analyze                   metrics.json + RESULTS-tables.md (decision rules of plan section 3)
Copied from the Stage 2 harness ($SP/p11/harness.py); the arm-3 wrapper, briefs and audit brief are kept byte-for-byte.
D2: cost decides on the loop only (R_LOOP); R_B is printed beside it.  D3: every record carries `stratum`.
D4: `build --extend`.  D6: no mid-run cost check exists anywhere in this tooling."""
import collections
import contextlib
import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
import statistics
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import score_themes as sc  # noqa: E402
from score_themes import blocking_findings, ids_from, parse_ids  # noqa: E402,F401

S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S/"scratchpad"; P11 = SP/"p11"
P12 = SP/"p12"; AB = P12/"ab2"; RUNS = AB/"runs"
S1 = SP/"exp346/.dev/experiments/346-validation/phase2/S1"
REPO = str(AB/"repo")                       # git_show reads the private clone
BASE_REF = "69ac8b3335564fb5551980e984c5d9b763039cc1"   # frozen audit command
PRODUCT_REF = "3d2fe006c00e71460ab7d56542fa01e29e7ce43e"     # test-arm command + rules file
SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
AUD_CMD_SHA = "e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494"
AUD_RULES_SHA = "3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8"
TASKS_GLOB = os.environ.get("AB_TASKS_GLOB", "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output")
MAX_CONCURRENT = int(os.environ.get("AB_MAX", "6"))
DESIGN = "b2"
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
STEPS = ["R1", "VF1", "V1", "R2", "VF2", "V2", "R3", "VF3", "AUD", "AUD2"]
LOOP_STEPS = [s for s in STEPS if not s.startswith("AUD")]
OUT = {3: {"R1": f"{D}/review/round1.md", "V1": f"{D}/review/revise1.md", "R2": f"{D}/review/round2.md",
           "V2": f"{D}/review/revise2.md", "R3": f"{D}/review/round3.md"}}
AUD_OUT = f"{D}/review/audit.md"
FLAGS = "--mode critique --focus requirements,architecture"


# ---------------------------------------------------------------- small helpers
def git_show(ref, path):
    return subprocess.run(["git", "-C", REPO, "show", f"{ref}:{path}"], check=True, capture_output=True, text=True).stdout


def run_dir(run): return RUNS/run
def arm_of(run): return 3
def stratum_of(run): return "haiku" if run.startswith("b2h-") else "sonnet"
def load(run): return json.load(open(run_dir(run)/"state.json"))
def save(run, st): json.dump(st, open(run_dir(run)/"state.json", "w"), indent=1)
def ws(run): return run_dir(run)/"ws"
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def sha_text(t): return hashlib.sha256(t.encode()).hexdigest()
def now_iso(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
def decision(): return json.load(open(AB/"decision.json"))


def spec_stats(run, base=None):
    p = (base or ws(run))/SPEC; b = p.read_bytes()
    return {"bytes": len(b), "lines": b.count(b"\n"), "sha256": hashlib.sha256(b).hexdigest()}


def section(text, title):
    m = re.search(rf"^### {re.escape(title)}\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    return m.group(1).strip()


def run_names():
    if not RUNS.exists():
        return []
    def key(r):
        m = re.match(r"b2(h?)-r(\d+)$", r)
        return (1 if m.group(1) else 0, int(m.group(2))) if m else (2, 0)
    return sorted((p.name for p in RUNS.iterdir() if (p/"state.json").exists()), key=key)


def loop_model_of(st, step):
    return "sonnet" if step.startswith("AUD") else st["loop_model"]


# ---------------------------------------------------------------- build
def metrics_json():
    p = AB/"metrics.json"
    return json.load(open(p)) if p.exists() else {}


def build(stratum="sonnet", extend=False):
    dec = decision()
    if extend:
        if stratum != "sonnet":
            sys.exit("--extend is Sonnet only")
        if metrics_json().get("sonnet_n6_outcome") != "INCONCLUSIVE":
            sys.exit("REFUSED: --extend needs $AB/metrics.json to record a Sonnet n=6 outcome of INCONCLUSIVE")
        if (RUNS/"b2-r7").exists():
            sys.exit("REFUSED: b2-r7 exists; the extension runs once")
        names = [f"b2-r{k}" for k in range(dec["N_SONNET"] + 1, dec["N_SONNET"] + dec["N_EXTEND"] + 1)]
    elif stratum == "haiku":
        names = [f"b2h-r{k}" for k in range(1, dec["N_HAIKU"] + 1)]
    else:
        names = [f"b2-r{k}" for k in range(1, dec["N_SONNET"] + 1)]
    cmd = git_show(PRODUCT_REF, "src/superclaude/commands/spec-panel.md")
    rules = git_show(PRODUCT_REF, "src/superclaude/rules/prompts/document_review_loop_prompts.md")
    for run in names:
        d = run_dir(run)
        if d.exists():
            print("skip existing", run); continue
        (d/"home/.claude/rules/prompts").mkdir(parents=True)
        shutil.copytree(S1/"inputs/repo-overlay", d/"ws")
        (d/"ws"/D/"review").mkdir(parents=True); (d/"ws"/D/"specs/history").mkdir(parents=True)
        assert sha(d/"ws"/SPEC) == SPEC_SHA, "spec sha mismatch"
        (d/"command.md").write_text(cmd)
        (d/"home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules)
        st = stratum_of(run)
        save(run, {"run": run, "design": DESIGN, "rep": int(run.split("-r")[1]), "stratum": st, "loop_model": st,
                   "product_ref": PRODUCT_REF, "cmd_sha": sha_text(cmd), "rules_sha": sha_text(rules),
                   "done": [], "log": {}, "launched": {}, "pending": [], "noted_unactioned": [],
                   "loop_end": None, "manual": [], "manual_ids": {}, "relaunch": {}, "lost": False, "complete": False})
    print("built", names)


# ---------------------------------------------------------------- briefs (arm 3 branches kept as in p11)
CTX = (f"First read {D}/README.md (binding shared context; the files under {D}/inventory/ are the only evidence you can check, "
       f"mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file(s).")


def new_brief(run, step, ids, out=None, prior=None, base=None, rep=None):
    a = arm_of(run); spec = SPEC; H = f"{D}/specs/history"
    ctx = CTX
    if step == "R1":
        out = out or OUT[a]["R1"]
        head = f"Run /sc:spec-panel @{spec} {FLAGS} ."
        body = (f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={spec}.")
        return f"{head} {body}\nWrite the full report to {out}. Do not edit anything else. {ctx}"
    if step in ("R2", "R3"):
        n = 2 if step == "R2" else 3
        prior = prior or OUT[a]["R1" if n == 2 else "R2"]; base = base or f"{H}/spec-v{n-1}.md"
        out = out or OUT[a][step]
        head = f"Run /sc:spec-panel @{spec} {FLAGS} --re-review {prior} --baseline {base} ."
        body = (f"Re-review per the RE-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. "
                f"Values: candidate={spec}, baseline={base}, prior={prior}.")
        return f"{head} {body}\nWrite the full report to {out}. Do not edit anything else. {ctx}"
    if step in ("V1", "V2"):
        n = 1 if step == "V1" else 2
        rep = rep or OUT[a]["R1" if n == 1 else "R2"]; out = out or OUT[a][step]
        vals = {"CANDIDATE": spec, "IDS": ids or "the blocking findings listed in the report"}
        body = (f"Revise per the REVISE prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. "
                f"Values: candidate={spec}, IDS={vals['IDS']}.")
        return (f"{body}\nInputs: the review report {rep} (its Reviser brief lists the blocking ids), the spec, and the files under {D}/inventory/. "
                f"Edit the spec {spec} in place; it is the only file you may change besides your output. Do not run the spec-panel. "
                f"Write {out} with the byte accounting the prompt asks for and one row per finding id (applied where, or rejected with a cited reason). {ctx}")
    raise ValueError(step)


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


# ---------------------------------------------------------------- ids and findings
def ids_for(run, n):
    """Blocking ids of review n: manual override first, else parsed from the report."""
    st = load(run)
    man = st.get("manual_ids", {}).get(f"R{n}")
    if man:
        return parse_ids(man)
    return parse_ids(ids_from(ws(run)/OUT[3][f"R{n}"]))


DROP_LINE = re.compile(r"(?i)^\s*(?:[-*]\s*)?(?:\*\*)?\s*(recommendation|rationale|experts?|priority|quality impact|why blocking|suggested fix)\b")


def findings(run, n):
    """The finding list the verifier sees (B5). Returns (text, ids)."""
    src = (ws(run)/OUT[3][f"R{n}"]).read_text(errors="ignore")
    ids = ids_for(run, n)
    parts = []
    for fid in ids:
        heading, body = sc.find_section(src, fid)
        lines = []
        if heading is not None:
            lines = [ln for ln in (body or "").splitlines()]
            if not any(ln.strip() for ln in lines) and n > 1:
                for prev in (f"round{n-1}.orig.md", f"round{n-1}.md"):
                    pp = ws(run)/D/"review"/prev
                    if pp.exists():
                        h2, b2 = sc.find_section(pp.read_text(errors="ignore"), fid)
                        if h2 is not None and any(x.strip() for x in (b2 or "").splitlines()):
                            lines += ["(text of this finding in the prior report)", h2] + b2.splitlines()
                            break
        else:
            hits = [ln for ln in src.splitlines() if re.search(r"(?<![\w-])" + re.escape(fid) + r"(?![\w-])", ln)][:10]
            heading, lines = (hits[0] if hits else fid), hits[1:]
        lines = [ln for ln in lines if not DROP_LINE.match(ln)]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        parts.append("\n".join([f"### {fid}", heading] + lines))
    text = "\n\n".join(parts)
    return text, ids


def parse_verify(text, ids):
    res = {}
    cl = re.findall(r"(?im)^\W*confirmed:\s*(.*)$", text)
    clist = None
    if cl:
        clist = [x for x in re.findall(r"[\w-]+", cl[-1]) if x.lower() != "none"]
    any_signal = bool(cl)
    for fid in ids:
        rx = re.compile(r"(?<![\w-])" + re.escape(fid) + r"(?![\w-])")
        row = None
        for ln in text.splitlines():
            if rx.search(ln) and re.search(r"(?i)\b(confirm|reject)", ln) and not re.match(r"(?i)^\W*confirmed:", ln):
                row = ln; break
        if row is not None:
            any_signal = True
            verdict = "reject" if re.search(r"(?i)\breject", row) else "confirm"
            cells = [c.strip() for c in row.split("|") if c.strip()]
            reason = cells[-1] if "|" in row and cells else row.strip()
            res[fid] = (verdict, reason)
        elif cl:
            res[fid] = ("confirm", "") if fid in clist else ("reject", "not in confirmed line")
    if not any_signal:
        return {fid: ("confirm", "no parseable reply; failing closed") for fid in ids}, False
    for fid in ids:
        res.setdefault(fid, ("confirm", "no row for this id; failing closed"))
    return res, True


# ---------------------------------------------------------------- prep
def _verify_brief_text():
    rules = git_show(PRODUCT_REF, "src/superclaude/rules/prompts/document_review_loop_prompts.md")
    m = re.search(r'- Verify brief: "([^"]+)"', rules)
    assert m, "no Verify brief in the rules file at PRODUCT_REF"
    return m.group(1)


def prep_audit(run, k):
    d = run_dir(run); sub = "aud" if k == 1 else "aud2"
    ad = d/sub
    if ad.exists():
        shutil.rmtree(ad)
    (ad/"home/.claude/rules/prompts").mkdir(parents=True)
    shutil.copytree(S1/"inputs/repo-overlay", ad/"ws")
    (ad/"ws"/D/"review").mkdir(parents=True)
    shutil.copy(ws(run)/SPEC, ad/"ws"/SPEC)
    git_cmd = git_show(BASE_REF, "src/superclaude/commands/spec-panel.md")
    assert sha_text(git_cmd) == AUD_CMD_SHA, "audit command sha mismatch"
    frozen = (P11/"rules.md").read_text()
    assert sha_text(frozen) == AUD_RULES_SHA, "audit rules sha mismatch"
    (ad/"command.md").write_text(git_cmd)
    (ad/"home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(frozen)
    brief = (f"Run /sc:spec-panel @{SPEC} {FLAGS} . This is a labelled whole-document audit of the final spec: a first review of the whole document. "
             f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={SPEC}.\n"
             f"Write the full report to {AUD_OUT}. Do not edit anything else. First read {D}/README.md (binding shared context; the files under {D}/inventory/ "
             f"are the only evidence you can check, mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file.")
    return ad, brief, CMDPART


def prep_verify(run, n):
    d = run_dir(run); vd = d/f"vf{n}"
    if vd.exists():
        shutil.rmtree(vd)
    spec_dst = vd/"ws"/SPEC
    spec_dst.parent.mkdir(parents=True)
    (vd/"ws"/D/"review").mkdir(parents=True); (vd/"home").mkdir(parents=True)
    shutil.copy(ws(run)/SPEC, spec_dst)
    ftext, ids = findings(run, n)
    (ws(run)/D/"review"/f"findings-{n}.md").write_text(ftext + "\n")
    st = load(run); st["log"].setdefault(f"VF{n}", {})["finding_ids"] = ids; save(run, st)
    b = _verify_brief_text().replace("{{CANDIDATE}}", SPEC).replace("{{FINDINGS}}", "\n\n" + ftext + "\n")
    b += f"\nWrite your full reply to {D}/review/verify-{n}.md. Do not edit anything else. Write only your output file."
    return vd, b, ""


def prep(run, step, subs=None):
    subs = subs or {}
    d = run_dir(run); st = load(run)
    if step in ("AUD", "AUD2"):
        sb, brief, cmdpart = prep_audit(run, 1 if step == "AUD" else 2)
        st = load(run); st["final_spec"] = spec_stats(run); save(run, st)
    elif step.startswith("VF"):
        sb, brief, cmdpart = prep_verify(run, int(step[2:]))
    else:
        sb, cmdpart = d, (CMDPART if step in ("R1", "R2", "R3") else "")
        if step in ("V1", "V2"):
            n = int(step[1])
            shutil.copy(ws(run)/SPEC, ws(run)/D/"specs/history"/f"spec-v{n}.md")
            ids = subs.get("IDS")
            if not ids:
                conf = st["log"].get(f"VF{n}", {}).get("confirmed")
                ids = ", ".join(conf) if conf else None
            print("IDS =", ids)
            brief = new_brief(run, step, ids)
        else:
            brief = new_brief(run, step, None)
    text = WRAP.format(sb=sb, wsdir="ws", cmdpart=cmdpart.format(sb=sb) if cmdpart else "", brief=brief)
    p = d/f"PROMPT-{step}.md"; p.write_text(text); print(p)
    return p


# ---------------------------------------------------------------- ingest
def out_path(run, step):
    d = run_dir(run)
    if step == "AUD":
        return d/"aud"/"ws"/AUD_OUT
    if step == "AUD2":
        return d/"aud2"/"ws"/AUD_OUT
    if step.startswith("VF"):
        return d/f"vf{step[2:]}"/"ws"/D/"review"/f"verify-{step[2:]}.md"
    return ws(run)/OUT[3][step]


def theme_overrides():
    p = AB/"theme-overrides.json"
    return json.load(open(p)) if p.exists() else {}


def ingest(run, step):
    st = load(run); outp = out_path(run, step)
    rec = {"output_exists": outp.exists(), "stratum": st["stratum"]}
    old = st["log"].get(step, {})
    for k in ("finding_ids", "output_tokens"):
        if k in old:
            rec[k] = old[k]
    if outp.exists():
        t = outp.read_text(errors="ignore"); rec["report_bytes"] = len(t.encode())
        if step in ("R1", "R2", "R3", "AUD", "AUD2"):
            rec["verdict"] = sc.verdict_of(t)
            rec["review_header"] = re.findall(r"^\W*review:\s*(\d)\s*of\s*3", t, re.I | re.M)
            rec["labels"] = dict(collections.Counter(re.findall(r"\b(CRITICAL|MAJOR|MINOR)\b", t)))
            rec["blocking_ids"] = ids_from(outp)
            if rec["verdict"] == "FAIL":
                rec["blocking"] = [{"id": f["id"], "heading": f["heading"], "theme": f["theme"], "cited": sorted(f["cited"])}
                                   for f in blocking_findings(outp)]
            else:
                rec["blocking"] = []
            if step in ("R1", "R2", "R3"):
                rec["ids"] = ids_for(run, int(step[1]))
    if step.startswith("VF") and outp.exists():
        rec.update(_ingest_verify(run, st, int(step[2:]), outp, rec))
    if step in ("R1", "R2", "R3", "V1", "V2"):
        rec["spec_after"] = spec_stats(run)
    st = load(run) if step.startswith("VF") else st   # _ingest_verify saves
    st["log"][step] = {**st["log"].get(step, {}), **rec}
    if step not in st["done"]:
        st["done"].append(step)
    save(run, st)
    print(json.dumps({run: {step: {k: v for k, v in rec.items() if k not in ("blocking",)}}}, indent=1))
    return rec


def _ingest_verify(run, st, n, outp, rec):
    reply = outp.read_text(errors="ignore")
    revdir = ws(run)/D/"review"
    shutil.copy(outp, revdir/f"verify-{n}.md")
    rpt = revdir/f"round{n}.md"; orig = revdir/f"round{n}.orig.md"
    if not orig.exists():
        shutil.copy(rpt, orig)
    ids = st["log"].get(f"VF{n}", {}).get("finding_ids") or ids_for(run, n)
    parsed, ok = parse_verify(reply, ids)
    print(f"parsed verifier table {run} VF{n} parse_ok={ok}")
    for fid in ids:
        print(f"   {fid}: {parsed[fid][0]} | {parsed[fid][1][:140]}")
    confirmed = [i for i in ids if parsed[i][0] == "confirm"]
    rejected = {i: parsed[i][1] for i in ids if parsed[i][0] == "reject"}
    c_txt = ", ".join(confirmed) if confirmed else "none"
    r_txt = "; ".join(f"{i} (verifier: {r})" for i, r in rejected.items()) if rejected else "none"
    block = (f"> verification (coordinator, VERIFY step VF{n}; verifier reply {D}/review/verify-{n}.md): confirmed blocking ids: {c_txt}. "
             f"Rejected, kept as noted, unactioned and not prior blocking findings for the next re-review: {r_txt}. "
             f"The Reviser brief below is narrowed to the confirmed ids.")
    lines = orig.read_text(errors="ignore").splitlines()
    at = next((i for i, ln in enumerate(lines) if re.match(r"^\W*review:\s*\d\s*of\s*3", ln, re.I)), None)
    lines.insert(0 if at is None else at + 1, block)
    rpt.write_text("\n".join(lines) + "\n")
    otext = orig.read_text(errors="ignore")
    st = load(run)
    st["noted_unactioned"] = [x for x in st["noted_unactioned"] if x["step"] != f"VF{n}"]
    for fid, reason in rejected.items():
        heading, body = sc.find_section(otext, fid)
        st["noted_unactioned"].append({"step": f"VF{n}", "id": fid, "theme": sc.tag(heading, body),
                                       "cited": sorted(sc.cited((heading or "") + "\n" + (body or ""))),
                                       "heading": heading, "reason": reason})
    save(run, st)
    with open(run_dir(run)/"NOTED.md", "w") as f:
        f.write("# Noted, unactioned (rejected by the verifier)\n\n| step | id | theme | heading | verifier reason |\n|---|---|---|---|---|\n")
        for x in st["noted_unactioned"]:
            f.write(f"| {x['step']} | {x['id']} | {x['theme']} | {(x['heading'] or '').replace('|', '/')} | {x['reason'].replace('|', '/')} |\n")
    return {"finding_ids": ids, "confirmed": confirmed, "rejected": rejected, "parse_ok": ok}


def setids(run, step, raw):
    st = load(run)
    st.setdefault("manual", []).append({"step": step, "ids": raw, "time": now_iso()})
    st.setdefault("manual_ids", {})[step] = raw
    save(run, st)
    print(f"manual ids recorded for {run} {step}: {parse_ids(raw)}")


def requeue(run, step, reason=""):
    """Drop a launch-ledger entry and re-queue the step; a second time marks the run lost (B2 items 7, 8)."""
    st = load(run)
    n = st.setdefault("relaunch", {}).get(step, 0)
    st["launched"].pop(step, None)
    st["log"].pop(step, None)
    if step in st["done"]:
        st["done"].remove(step)
    if n >= 1:
        st["lost"] = True
        st["lost_reason"] = f"{step}: second failure ({reason})"
        st["pending"] = []
        save(run, st); print(f"LOST {run}: {st['lost_reason']}"); return "lost"
    st["relaunch"][step] = n + 1
    st.setdefault("manual", []).append({"step": step, "relaunch": True, "reason": reason, "time": now_iso()})
    if step not in st["pending"]:
        st["pending"].insert(0, step)
    save(run, st); print(f"re-queued {run} {step} (relaunch 1 of 1)"); return "requeued"


# ---------------------------------------------------------------- transcripts and tokens
FIRST_RX = r"^Read \S*?{pat}/runs/(?P<run>[\w-]+)/PROMPT-(?P<step>\w+)\.md and follow"


def scan_transcripts(glob_pat, root_pat, run_rx=r"[\w-]+"):
    """-> {(run, step): [ {file, tokens, models, done} ]}.  Tokens: each message.id counted once (max output_tokens)."""
    import glob as _g
    rx = re.compile(r"^Read \S*?" + root_pat + r"/runs/(?P<run>" + run_rx + r")/PROMPT-(?P<step>\w+)\.md and follow")
    found = collections.defaultdict(list)
    for f in _g.glob(glob_pat):
        try:
            fh = open(f, errors="ignore")
            first = None
            for line in fh:
                try:
                    dd = json.loads(line)
                except Exception:
                    continue
                if dd.get("type") == "user":
                    c = (dd.get("message") or {}).get("content")
                    first = c if isinstance(c, str) else None
                    break
            if not first:
                continue
            m = rx.match(first.strip())
            if not m:
                continue
            per_id = {}; models = set(); done = False; last_text = ""
            fh.seek(0)
            for line in fh:
                try:
                    dd = json.loads(line)
                except Exception:
                    continue
                msg = dd.get("message") or {}
                if msg.get("role") != "assistant":
                    continue
                if msg.get("model"):
                    models.add(msg["model"])
                u = msg.get("usage") or {}
                mid = msg.get("id") or f"noid-{dd.get('uuid')}"
                per_id[mid] = max(per_id.get(mid, 0), u.get("output_tokens") or 0)
                if isinstance(msg.get("content"), list):
                    for b in msg["content"]:
                        if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "SubagentHandback" \
                                and "DONE" in json.dumps(b.get("input")):
                            done = True
                        if isinstance(b, dict) and b.get("type") == "text":
                            last_text = b.get("text", "")
                elif isinstance(msg.get("content"), str):
                    last_text = msg["content"]
            if "DONE" in last_text:
                done = True
            found[(m.group("run"), m.group("step"))].append(
                {"file": f, "tokens": sum(per_id.values()), "models": sorted(models), "done": done})
        except OSError:
            continue
    return found


def pick_transcript(cands, expected_model, key=None, warn=True):
    keep = []
    for c in cands:
        if any(expected_model in m for m in c["models"]):
            keep.append(c)
        elif warn:
            print(f"WARN {key}: transcript {pathlib.Path(c['file']).name} ran on {c['models']}, expected {expected_model}; ignored")
    if not keep:
        return None
    if len(keep) > 1 and warn:
        print(f"WARN {key}: {len(keep)} transcripts; keeping the one with DONE and most tokens")
    keep.sort(key=lambda c: (c["done"], c["tokens"]), reverse=True)
    return keep[0]


def ab_transcripts():
    return scan_transcripts(TASKS_GLOB, r"p12/ab2", r"b2h?-r\d+")


def tokens():
    found = ab_transcripts()
    for run in run_names():
        st = load(run); ch = False
        for step in STEPS:
            cands = found.get((run, step))
            if not cands:
                continue
            c = pick_transcript(cands, loop_model_of(st, step), key=f"{run} {step}")
            if c is None:
                continue
            st["log"].setdefault(step, {})["output_tokens"] = c["tokens"]; ch = True
        if ch:
            save(run, st)
    print("tokens attached")


def basetokens(glob_pat=None):
    found = scan_transcripts(glob_pat or TASKS_GLOB, r"p11", r"a3-r\d")
    per = collections.defaultdict(dict)
    for (run, step), cands in found.items():
        c = pick_transcript(cands, "sonnet", key=f"{run} {step}", warn=False)
        if c:
            per[run][step] = c["tokens"]
    loops, auds = [], []
    for run in sorted(per):
        loop = sum(v for s, v in per[run].items() if s != "AUD"); aud = per[run].get("AUD", 0)
        loops.append(loop); auds.append(aud)
        print(f"{run}: loop {loop:,} audit {aud:,}  steps {per[run]}")
    if loops:
        print(f"MEAN loop {statistics.mean(loops):,.0f}  audit {statistics.mean(auds):,.0f}")
    return per


# ---------------------------------------------------------------- status
def status():
    for run in run_names():
        st = load(run); row = []
        for s in STEPS:
            r = st["log"].get(s)
            if r is None:
                row.append(f"{s}:{'L' if s in st['launched'] else '-'}")
            else:
                row.append(f"{s}:{r.get('verdict', 'ok' if r['output_exists'] else 'MISSING')}")
        flag = "LOST" if st.get("lost") else ("complete" if st.get("complete") else "")
        print(run, st["stratum"], " ".join(row), "| loop_end", st.get("loop_end"), flag)


# ---------------------------------------------------------------- analysis (D2, D3, D4, D6)
def cost_ratios(loop_mean, aud_mean, dec=None):
    """The one place where the cost convention lives.  R_LOOP decides; R_B is reported only (D2)."""
    dec = dec or decision()
    return {"R_LOOP": loop_mean/dec["A_BASE"], "R_B": (loop_mean + aud_mean)/dec["B_BASE"],
            "LOOP": loop_mean, "TOK": loop_mean + aud_mean}


def _frac(s):
    a, b = s.split("/"); return int(a)/int(b)


def baseline_stats(dec):
    """B_BLK, B_AUDFAIL, B_THEME over all existing baseline audits (audit 1 + audit 2)."""
    rd = pathlib.Path(dec["baseline_runs_dir"]); a2 = pathlib.Path(dec["baseline_audit2_dir"])
    aud = {1: {}, 2: {}}
    for k in range(1, 7):
        r = f"a3-r{k}"
        p1 = rd/r/"aud/ws"/AUD_OUT
        if p1.exists():
            aud[1][r] = p1
        p2 = a2/r/"ws"/AUD_OUT
        if p2.exists():
            aud[2][r] = p2
    def stats(paths):
        fs = []
        for p in paths:
            t = pathlib.Path(p).read_text(errors="ignore")
            v = sc.verdict_of(t)
            if v not in ("PASS", "FAIL"):
                continue
            b = blocking_findings(p) if v == "FAIL" else []
            fs.append({"verdict": v, "blocking": b, "themes": {x["theme"] for x in b}})
        return fs
    def summarize(fs):
        if not fs:
            return None
        return {"n_audits": len(fs), "B_BLK": statistics.mean(len(f["blocking"]) for f in fs),
                "B_AUDFAIL": sum(f["verdict"] == "FAIL" for f in fs)/len(fs),
                "B_THEME": sum(bool(f["themes"] & {"T1", "T2", "T3"}) for f in fs)/len(fs),
                "audits_with_blocking": [(f["verdict"], [(x["id"], x["theme"]) for x in f["blocking"]]) for f in fs]}
    pooled = stats(list(aud[1].values()) + list(aud[2].values()))
    out = {"pooled": summarize(pooled), "audit1": summarize(stats(aud[1].values())),
           "audit2": summarize(stats(aud[2].values())), "have_audit2": bool(aud[2])}
    out["provisional"] = not aud[2]
    out["findings"] = {1: {r: blocking_findings(p) for r, p in aud[1].items()}, 2: {r: blocking_findings(p) for r, p in aud[2].items()}}
    if out["pooled"] is None:
        out["pooled"] = {"B_BLK": dec["B_BLK"], "B_AUDFAIL": _frac(dec["B_AUDFAIL"]), "B_THEME": _frac(dec["B_THEME"]), "n_audits": 0}
        out["provisional"] = True
    return out


def load_runs(stratum):
    """Per-run metric records for the completed runs of a stratum (theme overrides applied)."""
    ov = theme_overrides()
    runs = []
    for run in run_names():
        st = load(run)
        if st["stratum"] != stratum:
            continue
        rec = {"run": run, "stratum": stratum, "lost": st.get("lost", False), "complete": st.get("complete", False),
               "loop_end": st.get("loop_end"), "relaunch": sum(st.get("relaunch", {}).values()),
               "manual": len(st.get("manual", []))}
        if not rec["complete"] or rec["lost"]:
            runs.append(rec); continue
        lg = st["log"]
        rec["reviews"] = sum(1 for s in ("R1", "R2", "R3") if s in lg)
        rec["fix_cycles"] = sum(1 for s in ("V1", "V2") if s in lg)
        fb = st["final_spec"]["bytes"]
        rec["spec_bytes"] = fb; rec["growth_pct"] = (fb - 57763)/57763*100
        rec["LOOP"] = sum(lg[s].get("output_tokens", 0) for s in LOOP_STEPS if s in lg)
        rec["AUD_tokens"] = lg["AUD"].get("output_tokens", 0); rec["AUD2_tokens"] = lg["AUD2"].get("output_tokens", 0)
        rec["TOK"] = rec["LOOP"] + rec["AUD_tokens"]
        rec["tokens_missing"] = [s for s in lg if "output_tokens" not in lg[s]]
        for k, s in ((1, "AUD"), (2, "AUD2")):
            r = lg[s]
            items = []
            for b in r.get("blocking", []):
                th = ov.get(f"{run}/{'audit' if k == 1 else 'audit2'}/{b['id']}", b["theme"])
                items.append({**b, "theme": th})
            rec[f"aud{k}"] = {"verdict": r.get("verdict"), "blocking": items}
        rec["vf"] = {}
        for n in (1, 2, 3):
            v = lg.get(f"VF{n}")
            if v:
                rec["vf"][n] = {"sent": len(v.get("finding_ids", [])), "confirmed": v.get("confirmed", []),
                                "rejected": v.get("rejected", {}), "parse_ok": v.get("parse_ok")}
        rec["noted"] = st.get("noted_unactioned", [])
        runs.append(rec)
    return runs


def rej_true_rows(runs, which=(1, 2)):
    """Rejected findings matched against the blockers of the same run's audits; eyeball file overrides the automatic match."""
    p = AB/"rej-true-overrides.json"
    eye = json.load(open(p)) if p.exists() else {}
    rows = []
    for r in runs:
        if not r.get("complete") or r.get("lost"):
            continue
        for x in r["noted"]:
            hit = None
            for k in which:
                for b in r[f"aud{k}"]["blocking"]:
                    if sc.matches_audit({"theme": x["theme"], "cited": set(x["cited"])}, {"theme": b["theme"], "cited": set(b["cited"])}):
                        hit = f"AUD{k}:{b['id']}"; break
                if hit:
                    break
            key = f"{r['run']}/{x['step']}/{x['id']}"
            auto = hit is not None
            true = eye.get(key, auto)
            rows.append({"run": r["run"], "step": x["step"], "id": x["id"], "theme": x["theme"], "reason": x["reason"],
                         "match": hit, "auto": auto, "eyeballed": key in eye, "rej_true": bool(true)})
    return rows


def outcome_rules(runs, n_planned, bstats, dec, which=(1, 2)):
    """Section 3 rules in the pre-registered order for one set of audits (`which`).  Pure given its inputs."""
    rules = dec["rules"]; done = [r for r in runs if r.get("complete") and not r.get("lost")]
    res = {"n_planned": n_planned, "completed": len(done), "which": list(which)}
    if not done:
        res.update(outcome="INCONCLUSIVE", fired="no completed run"); return res
    blk = [len(r[f"aud{k}"]["blocking"]) for r in done for k in which]
    res["BLK_T"] = statistics.mean(blk)
    res["audits"] = len(blk)
    res["audits_pass"] = sum(1 for r in done for k in which if r[f"aud{k}"]["verdict"] == "PASS")
    res["audits_fail_rate"] = sum(1 for r in done for k in which if r[f"aud{k}"]["verdict"] == "FAIL")/len(blk)
    res["theme_rate"] = sum(1 for r in done for k in which
                            if {b["theme"] for b in r[f"aud{k}"]["blocking"]} & {"T1", "T2", "T3"})/len(blk)
    loop_mean = statistics.mean(r["LOOP"] for r in done)
    aud_mean = statistics.mean(r["AUD_tokens"] for r in done)
    res.update(cost_ratios(loop_mean, aud_mean, dec))
    res["loop_pass"] = sum(1 for r in done if r["loop_end"] in ("PASS", "VERIFIED-PASS"))
    res["loop_pass_split"] = {"PASS": sum(1 for r in done if r["loop_end"] == "PASS"),
                              "VERIFIED-PASS": sum(1 for r in done if r["loop_end"] == "VERIFIED-PASS"),
                              "ESCALATED": sum(1 for r in done if r["loop_end"] == "ESCALATED")}
    rows = rej_true_rows(done, which)
    n_ver = sum(v["sent"] for r in done for v in r["vf"].values())
    rej = sum(len(v["rejected"]) for r in done for v in r["vf"].values())
    rej_true = sum(1 for x in rows if x["rej_true"])
    res.update(N_VER=n_ver, REJ=rej, REJ_TRUE=rej_true, REJ_TRUE_RATE=(rej_true/n_ver if n_ver else 0.0))
    b_blk = bstats["B_BLK"]; limit = dec["COST_LIMIT_R_LOOP"]
    res["B_BLK"] = b_blk; res["cost_limit"] = limit
    min_done = rules["MIN_COMPLETED"][str(n_planned)]
    pass_min = rules["DROP3_PASS_MIN"][str(n_planned)]
    fired = []
    if res["REJ_TRUE_RATE"] > rules["DROP1_REJ_TRUE_RATE_GT"]:
        fired.append("DROP-1")
    if res["BLK_T"] > rules["DROP2_BLK_FACTOR_GT"]*b_blk and res["R_LOOP"] > limit:
        fired.append("DROP-2")
    if res["loop_pass"] < pass_min or res["BLK_T"] > rules["DROP3_BLK_FACTOR_GT"]*b_blk:
        fired.append("DROP-3")
    if len(done) < min_done:
        outcome = "INCONCLUSIVE"; why = f"fewer than {min_done} completed runs"
    elif fired:
        outcome = "DROP"; why = fired[0] + (" (also " + ", ".join(fired[1:]) + ")" if len(fired) > 1 else "")
    elif res["BLK_T"] <= rules["ADOPT_BLK_FACTOR_LE"]*b_blk and res["R_LOOP"] <= limit and rej >= rules["ADOPT_REJ_MIN"]:
        outcome = "ADOPT"; why = "ADOPT conditions met"
    elif rej == 0:
        outcome = "INCONCLUSIVE"; why = "REJ = 0: the gate never acted (no effect observed)"
    else:
        outcome = "INCONCLUSIVE"; why = "no DROP rule fired and the ADOPT conditions are not all met"
    res.update(outcome=outcome, fired=why, drops=fired)
    return res


def _baseline_for(bs, which):
    if len(which) == 2:
        return bs["pooled"]
    k = which[0]
    return bs["audit1" if k == 1 else "audit2"] or bs["pooled"]


def haiku_baseline(dec):
    p = pathlib.Path(dec["haiku_baseline_json"])
    if not p.exists():
        return None
    raw = json.load(open(p))
    runs = raw.get("runs", raw) if isinstance(raw, dict) else raw
    items = list(runs.items()) if isinstance(runs, dict) else [(x.get("run", i), x) for i, x in enumerate(runs)]
    items = [(k, v) for k, v in items if isinstance(v, dict)]
    base_dir = p.parent/"runs"
    blks, loops, growth, fails, passes = [], [], [], 0, 0
    for k, v in items:
        rescored = None
        a1, a2 = base_dir/k/"aud/ws"/AUD_OUT, base_dir/k/"aud2/ws"/AUD_OUT
        if a1.exists() and a2.exists():
            rescored = statistics.mean(len(blocking_findings(a)) for a in (a1, a2))
        if rescored is None:
            for key in ("blocking_per_audit", "mean_blocking", "n_blocking_mean"):
                if key in v:
                    rescored = float(v[key]); break
            else:
                nb = v.get("n_blocking") or v.get("blocking_counts") or v.get("audit_blocking")
                if isinstance(nb, (list, tuple)) and nb:
                    rescored = statistics.mean(nb)
                elif isinstance(nb, (int, float)):
                    rescored = float(nb)
        if rescored is not None:
            blks.append(rescored)
        for key in ("loop_tokens", "LOOP", "loop"):
            if key in v:
                loops.append(float(v[key])); break
        if "growth_pct" in v:
            growth.append(float(v["growth_pct"]))
        if v.get("loop_end", v.get("loop_pass")) in ("PASS", "VERIFIED-PASS", True):
            passes += 1
        if v.get("lost") or v.get("manual") or v.get("relaunch"):
            fails += 1
    if not blks:
        return {"usable": False, "path": str(p)}
    return {"usable": True, "path": str(p), "n": len(items), "H_BLK": statistics.mean(blks),
            "H_LOOP": statistics.mean(loops) if loops else None,
            "growth": statistics.mean(growth) if growth else None,
            "loop_pass": passes, "fail_rate": fails/len(items) if items else 0.0}


def analyze():
    dec = decision(); bs = baseline_stats(dec)
    extended = (RUNS/"b2-r7").exists()
    n_planned = dec["N_SONNET"] + (dec["N_EXTEND"] if extended else 0)
    sruns = load_runs("sonnet"); hruns = load_runs("haiku")
    full = outcome_rules(sruns, n_planned, bs["pooled"], dec)
    r1 = outcome_rules(sruns, n_planned, _baseline_for(bs, (1,)), dec, which=(1,))
    r2 = outcome_rules(sruns, n_planned, _baseline_for(bs, (2,)), dec, which=(2,))
    pre_haiku = full["outcome"]; why = full["fired"]
    agreement = r1["outcome"] == r2["outcome"]
    if not agreement:
        pre_haiku = "INCONCLUSIVE"; why = f"replica disagreement: audit-1-only {r1['outcome']}, audit-2-only {r2['outcome']}"
    # Haiku stratum (3b): secondary, never pooled
    hb = haiku_baseline(dec)
    h = {"runs": len(hruns), "complete": sum(1 for r in hruns if r.get("complete") and not r.get("lost"))}
    hdone = [r for r in hruns if r.get("complete") and not r.get("lost")]
    if hdone:
        h["BLK_TH"] = statistics.mean(len(r[f"aud{k}"]["blocking"]) for r in hdone for k in (1, 2))
        h["loop_pass"] = sum(1 for r in hdone if r["loop_end"] in ("PASS", "VERIFIED-PASS"))
        h["growth_pct"] = statistics.mean(r["growth_pct"] for r in hdone)
        h["LOOP_TH"] = statistics.mean(r["LOOP"] for r in hdone)
        h["verifier_rejections"] = sum(len(v["rejected"]) for r in hdone for v in r["vf"].values())
        h["verifier_sent"] = sum(v["sent"] for r in hdone for v in r["vf"].values())
    h["harness_failure_rate"] = (sum(1 for r in hruns if r.get("lost") or r.get("relaunch") or r.get("manual"))/len(hruns)) if hruns else None
    haiku_state = "pending"
    if hb and hb.get("usable") and hdone:
        h["H_BLK"] = hb["H_BLK"]; h["HR"] = h["BLK_TH"]/hb["H_BLK"] if hb["H_BLK"] else None
        h["one_minus_HR"] = None if h["HR"] is None else 1 - h["HR"]
        h["R_LOOP_H"] = h["LOOP_TH"]/hb["H_LOOP"] if hb.get("H_LOOP") else None
        h["baseline_fail_rate"] = hb["fail_rate"]
        ok = (h["one_minus_HR"] is not None and h["one_minus_HR"] > 0
              and h["harness_failure_rate"] <= hb["fail_rate"] + dec["haiku"]["HARNESS_FAIL_MARGIN"])
        haiku_state = "agrees" if ok else "disagrees"
    final = pre_haiku
    if pre_haiku == "ADOPT":
        if haiku_state == "pending":
            final = "ADOPT (Haiku robustness pending)"
        elif haiku_state == "disagrees":
            final = "INCONCLUSIVE"; why = "Haiku stratum disagrees (ADOPT on Sonnet withdrawn)"
    if extended and final == "INCONCLUSIVE":
        why += "; extension already used, final verdict INCONCLUSIVE (no second extension without the owner)"
    key = "sonnet_n9" if extended else "sonnet_n6"
    m = metrics_json()
    m.update({"stratum_sonnet": {"n_planned": n_planned, "full": full, "audit1_only": r1, "audit2_only": r2}, "haiku": h,
              "baseline": {k: v for k, v in bs.items() if k != "findings"}, "provisional": bs["provisional"]})
    finished = len(sruns) >= n_planned and all(r.get("complete") or r.get("lost") for r in sruns)
    m[f"{key}_outcome"] = pre_haiku if finished else "PENDING"      # frozen only once every Sonnet run is complete or lost
    m[f"{key}_final"] = final if finished else "PENDING"
    m["extension_allowed"] = finished and (not extended) and pre_haiku == "INCONCLUSIVE"
    m["final_outcome"] = final
    json.dump(m, open(AB/"metrics.json", "w"), indent=1, default=str)
    _write_tables(dec, bs, sruns, hruns, full, r1, r2, final, why, pre_haiku, agreement, h, hb, haiku_state, extended)
    print(f"OUTCOME {final} ({why})")
    print(f"R_LOOP {full.get('R_LOOP', float('nan')):.3f}  R_B {full.get('R_B', float('nan')):.3f}  BLK_T {full.get('BLK_T', float('nan')):.2f}")
    return m


def _f(x, nd=2):
    return "n/a" if x is None else (f"{x:,.{nd}f}" if isinstance(x, float) else f"{x:,}" if isinstance(x, int) else str(x))


def _write_tables(dec, bs, sruns, hruns, full, r1, r2, final, why, pre_haiku, agreement, h, hb, haiku_state, extended):
    L = []
    prov = " PROVISIONAL (single baseline audit)" if bs["provisional"] else ""
    L.append(f"# RESULTS-tables (generated by harness.py analyze)\n\nOutcome: **{final}**{prov}{' n=9' if extended else ''}; rule: {why}\n")
    if "R_LOOP" in full:
        L.append(f"Cost: R_LOOP = {full['R_LOOP']:.3f} (decides; limit {dec['COST_LIMIT_R_LOOP']}), R_B = {full['R_B']:.3f} (reported only). "
                 f"Cost is judged post-hoc, after the runs completed.\n")
    pb = bs["pooled"]
    L.append(f"Baseline used: B_BLK {pb['B_BLK']:.2f}, B_AUDFAIL {pb['B_AUDFAIL']:.2f}, B_THEME {pb['B_THEME']:.2f} over {pb['n_audits']} audits "
             f"(audit-2 present: {bs['have_audit2']}).\n")
    L.append("## Analysis table (Sonnet stratum)\n")
    L.append("| Metric | Baseline a3 | Test b2 | Rule |\n|---|---|---|---|")
    if "BLK_T" in full:
        L.append(f"| Loop PASS (PASS + VERIFIED-PASS) | {dec['B_PASS']} | {full['loop_pass']}/{full['n_planned']} {full['loop_pass_split']} | DROP-3 below {dec['rules']['DROP3_PASS_MIN'][str(full['n_planned'])]} |")
        done = [r for r in sruns if r.get('complete') and not r.get('lost')]
        L.append(f"| Mean reviews | {dec['B_REV']} | {statistics.mean(r['reviews'] for r in done):.2f} | report |")
        L.append(f"| Mean fix cycles | {dec['B_FIX_CYCLES']} | {statistics.mean(r['fix_cycles'] for r in done):.2f} | report |")
        L.append(f"| Mean growth % | +{dec['B_GROWTH_PCT']} | {statistics.mean(r['growth_pct'] for r in done):+.2f} | report |")
        L.append(f"| Mean LOOP (A) / R_LOOP | {dec['A_BASE']:,} / 1.00 | {full['LOOP']:,.0f} / {full['R_LOOP']:.3f} | <= {dec['COST_LIMIT_R_LOOP']} |")
        L.append(f"| Mean TOK (B) / R_B | {dec['B_BASE']:,} / 1.00 | {full['TOK']:,.0f} / {full['R_B']:.3f} | report only |")
        L.append(f"| Audits PASS | {pb['n_audits'] - round(pb['B_AUDFAIL']*pb['n_audits'])}/{pb['n_audits']} | {full['audits_pass']}/{full['audits']} | report |")
        L.append(f"| BLK_T pooled / audit 1 / audit 2 | {pb['B_BLK']:.2f} | {full['BLK_T']:.2f} / {r1['BLK_T']:.2f} / {r2['BLK_T']:.2f} | ADOPT <= {dec['rules']['ADOPT_BLK_FACTOR_LE']}x; DROP-2 > {dec['rules']['DROP2_BLK_FACTOR_GT']}x with cost; DROP-3 > {dec['rules']['DROP3_BLK_FACTOR_GT']}x |")
        L.append(f"| Audit FAIL rate / theme rate | {pb['B_AUDFAIL']:.2f} / {pb['B_THEME']:.2f} | {full['audits_fail_rate']:.2f} / {full['theme_rate']:.2f} | report |")
        L.append(f"| N_VER, REJ, REJ_TRUE, REJ_TRUE/N_VER | n/a | {full['N_VER']}, {full['REJ']}, {full['REJ_TRUE']}, {full['REJ_TRUE_RATE']:.3f} | DROP-1 > {dec['rules']['DROP1_REJ_TRUE_RATE_GT']}; ADOPT needs REJ >= {dec['rules']['ADOPT_REJ_MIN']} |")
    L.append(f"\nReplica agreement: audit-1-only {r1.get('outcome')}, audit-2-only {r2.get('outcome')} -> {'agree' if agreement else 'DISAGREE'}.\n")
    L.append("## Per run (Sonnet)\n\n| run | loop end | reviews | fix cycles | growth % | LOOP | AUD tok | AUD verdict / blockers | AUD2 verdict / blockers |\n|---|---|---|---|---|---|---|---|---|")
    for r in sruns:
        if not r.get("complete") or r.get("lost"):
            L.append(f"| {r['run']} | {'LOST' if r.get('lost') else 'incomplete'} | | | | | | | |"); continue
        a = lambda k: f"{r[f'aud{k}']['verdict']} " + ", ".join(f"{b['id']} {b['theme']}" for b in r[f'aud{k}']['blocking'])
        L.append(f"| {r['run']} | {r['loop_end']} | {r['reviews']} | {r['fix_cycles']} | {r['growth_pct']:+.2f} | {r['LOOP']:,} | {r['AUD_tokens']:,} | {a(1)} | {a(2)} |")
    L.append("\n## Verifier table\n\n| run | step | sent | confirmed | rejected | parse_ok |\n|---|---|---|---|---|---|")
    for r in sruns + hruns:
        for n, v in sorted(r.get("vf", {}).items()):
            L.append(f"| {r['run']} | VF{n} | {v['sent']} | {', '.join(v['confirmed']) or 'none'} | {', '.join(v['rejected']) or 'none'} | {v['parse_ok']} |")
    L.append("\n## Noted, unactioned vs audits (rejected findings)\n\n| run | step | id | theme | verifier reason | matched audit blocker | auto/eyeballed | REJ_TRUE |\n|---|---|---|---|---|---|---|---|")
    for x in rej_true_rows(sruns):
        L.append(f"| {x['run']} | {x['step']} | {x['id']} | {x['theme']} | {x['reason'][:100]} | {x['match'] or 'none'} | {'eyeballed' if x['eyeballed'] else 'AUTO - eyeball me'} | {x['rej_true']} |")
    L.append("\n## Tagged audit findings (eyeball every tag)\n")
    for r in sruns + hruns:
        if r.get("complete") and not r.get("lost"):
            for k in (1, 2):
                for b in r[f"aud{k}"]["blocking"]:
                    L.append(f"- {r['run']} AUD{k} {b['id']} -> {b['theme']}: {(b['heading'] or '')[:120]}")
    L.append("\n## Haiku stratum (never pooled with Sonnet)\n")
    L.append("| Haiku baseline | Haiku test b2h | H_BLK | BLK_TH | HR | 1-HR | loop PASS | growth % | verifier rejections | harness failure rate (test / base) | R_LOOP_H |\n|---|---|---|---|---|---|---|---|---|---|---|")
    L.append(f"| {'n=' + str(hb['n']) if hb and hb.get('usable') else 'missing'} | n={h['complete']} complete of {h['runs']} | {_f(h.get('H_BLK'))} | {_f(h.get('BLK_TH'))} | {_f(h.get('HR'))} | {_f(h.get('one_minus_HR'))} | {_f(h.get('loop_pass'))} | {_f(h.get('growth_pct'))} | {_f(h.get('verifier_rejections'))}/{_f(h.get('verifier_sent'))} | {_f(h.get('harness_failure_rate'))} / {_f(h.get('baseline_fail_rate'))} | {_f(h.get('R_LOOP_H'))} |")
    L.append(f"\nHaiku state: {haiku_state}.\n")
    ab1 = pathlib.Path(dec["ab1_metrics_json"])
    if ab1.exists():
        L.append("## b1 (k=3 + verify), for information\n\nSee " + str(ab1) + "; the k ablation is analyzed in ab1.\n")
    (AB/"RESULTS-tables.md").write_text("\n".join(L) + "\n")


# ---------------------------------------------------------------- cli
def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    c = a[0]
    if c == "build":
        stratum = a[a.index("--stratum") + 1] if "--stratum" in a else "sonnet"
        build(stratum, "--extend" in a)
    elif c == "prep":
        prep(a[1], a[2], dict(kv.split("=", 1) for kv in a[3:]))
    elif c == "ingest":
        ingest(a[1], a[2])
    elif c == "setids":
        setids(a[1], a[2], a[3])
    elif c == "unlaunch":
        requeue(a[1], a[2], "manual unlaunch")
    elif c == "tokens":
        tokens()
    elif c == "basetokens":
        basetokens()
    elif c == "status":
        status()
    elif c == "analyze":
        analyze()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
