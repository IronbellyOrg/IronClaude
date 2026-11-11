#!/usr/bin/env python3
"""A/B 3 harness: arm-3 spec review loop plus a final whole-document gate with one bounded gate loop.
Copied from the Stage 2 harness ($SP/p11/harness.py); constants, WRAP, CMDPART and the arm-3 briefs are byte-for-byte the same.

Usage:
  harness.py build [--stratum sonnet|haiku] [--extend]   create sandboxes (b3-r1..6 | b3h-r1..4 | b3-r7..9)
  harness.py prep RUN STEP                               write RUN/PROMPT-STEP.md (STEP in R1 V1 R2 V2 R3 G GV GR AUD AUD2)
  harness.py ingest RUN STEP                             record outputs of a finished step
  harness.py setids RUN STEP "F1, F2"                    manual blocking ids for a review step (recorded in state["manual"])
  harness.py unlaunch RUN STEP                           remove a launch-ledger entry
  harness.py lose RUN                                    mark a run lost (excluded from analysis)
  harness.py eyeball RUN yes|no                          a person's judgement of a stall decision
  harness.py status | tokens | basetokens | analyze

D2 (token convention), D3 (strata) and D4 (extension) are implemented here; every threshold is read from decision.json.
D6: nothing in this file stops, truncates or skips work because of token or dollar cost.
"""
import datetime
import glob
import hashlib
import json
import math
import os
import pathlib
import re
import shutil
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import score_themes as st_  # noqa: E402

S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S / "scratchpad"; P11 = SP / "p11"
P12 = SP / "p12"; AB = P12 / "ab3"; RUNS = AB / "runs"
S1 = SP / "exp346/.dev/experiments/346-validation/phase2/S1"
REPO = str(AB / "repo")                                   # git_show reads the private clone
BASE_REF = "69ac8b3335564fb5551980e984c5d9b763039cc1"     # frozen audit command
PRODUCT_REF = "e924cc2b505da847c78d8580aa7daa17f4e15f2c"  # test-arm command + rules file (set after the A4 commit)
SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
AUD_CMD_SHA = "e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494"
AUD_RULES_SHA = "3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8"
TASKS_GLOB = os.environ.get("AB_TASKS_GLOB", "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output")
MAX_CONCURRENT = int(os.environ.get("AB_MAX", "6"))
DESIGN = "b3"

D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
STEPS = ["R1", "V1", "R2", "V2", "R3", "G", "GV", "GR", "AUD", "AUD2"]
LOOP_STEPS = ["R1", "V1", "R2", "V2", "R3", "G", "GV", "GR"]
REVIEW_STEPS = ("R1", "R2", "R3", "G", "GR")
REVISE_STEPS = ("V1", "V2", "GV")
OUT = {"R1": f"{D}/review/round1.md", "V1": f"{D}/review/revise1.md", "R2": f"{D}/review/round2.md",
       "V2": f"{D}/review/revise2.md", "R3": f"{D}/review/round3.md",
       "G": f"{D}/review/gate.md", "GV": f"{D}/review/revise-gate.md", "GR": f"{D}/review/gate-round2.md"}
AUD_OUT = f"{D}/review/audit.md"
FLAGS = "--mode critique --focus requirements,architecture"
H = f"{D}/specs/history"


def git_show(ref, path): return subprocess.run(["git", "-C", REPO, "show", f"{ref}:{path}"], check=True, capture_output=True, text=True).stdout
def run_dir(run): return RUNS / run
def arm_of(run): return 3          # every run takes the arm-3 pointer-brief path
def load(run): return json.load(open(run_dir(run) / "state.json"))
def save(run, st): json.dump(st, open(run_dir(run) / "state.json", "w"), indent=1)
def ws(run): return run_dir(run) / "ws"
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def spec_stats(run, base=None):
    p = (base or ws(run)) / SPEC; b = p.read_bytes()
    return {"bytes": len(b), "lines": b.count(b"\n"), "sha256": hashlib.sha256(b).hexdigest()}


def section(text, title):
    m = re.search(rf"^### {re.escape(title)}\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    return m.group(1).strip()


def cfg():
    return json.load(open(AB / "decision.json"))


def all_runs():
    if not RUNS.exists():
        return []
    return sorted((p.name for p in RUNS.iterdir() if (p / "state.json").exists()), key=run_key)


def run_key(run):
    m = re.match(r"b3(h?)-r(\d+)$", run)
    return (1 if m.group(1) else 0, int(m.group(2))) if m else (2, 0)


# ----------------------------------------------------------------------------- build
def build(stratum="sonnet", extend=False):
    c = cfg()
    if extend:
        if stratum != "sonnet":
            sys.exit("--extend is Sonnet only")
        mp = AB / "metrics.json"
        m = json.load(open(mp)) if mp.exists() else {}
        sn = (m.get("sonnet") or {})
        if sn.get("sonnet_outcome") != c["extension"]["allowed_when_sonnet_outcome"] or sn.get("n_planned") != c["N_SONNET"]:
            sys.exit(f"refused: --extend needs {mp} to record a Sonnet n={c['N_SONNET']} outcome of INCONCLUSIVE")
        if (RUNS / c["extension"]["run_names"][0]).exists():
            sys.exit("refused: the extension already exists (never extend twice without the owner)")
        names = list(c["extension"]["run_names"])
    elif stratum == "haiku":
        names = [f"b3h-r{i}" for i in range(1, c["N_HAIKU"] + 1)]
    else:
        names = [f"b3-r{i}" for i in range(1, c["N_SONNET"] + 1)]
    cmd_new = git_show(PRODUCT_REF, "src/superclaude/commands/spec-panel.md")
    rules = git_show(PRODUCT_REF, "src/superclaude/rules/prompts/document_review_loop_prompts.md")
    loop_model = c["strata"][stratum]["loop_model"]
    for run in names:
        d = run_dir(run)
        if d.exists():
            print("skip existing", run); continue
        (d / "home/.claude/rules/prompts").mkdir(parents=True)
        shutil.copytree(S1 / "inputs/repo-overlay", d / "ws")
        (d / "ws" / D / "review").mkdir(parents=True); (d / "ws" / D / "specs/history").mkdir(parents=True)
        assert sha(d / "ws" / SPEC) == SPEC_SHA, "spec sha mismatch"
        (d / "command.md").write_text(cmd_new)
        (d / "home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules)
        rep = int(re.search(r"-r(\d+)$", run).group(1))
        save(run, {"run": run, "design": DESIGN, "stratum": stratum, "loop_model": loop_model, "rep": rep,
                   "product_ref": PRODUCT_REF, "cmd_sha": hashlib.sha256(cmd_new.encode()).hexdigest(),
                   "rules_sha": hashlib.sha256(rules.encode()).hexdigest(), "done": [], "log": {}, "launched": {},
                   "noted_unactioned": [], "loop_end": None, "manual": []})
    print("built", names)


# ----------------------------------------------------------------------------- ids
def ids_from(report_path): return st_.ids_from(report_path)
def parse_ids(raw): return st_.parse_ids(raw)


def ids_for(run, step):
    """Blocking ids of a review step: manual (setids) first, else parsed from the report."""
    st = load(run)
    if st.get("ids", {}).get(step) is not None:
        return list(st["ids"][step])
    p = review_path(run, step)
    return parse_ids(ids_from(p)) if p.exists() else []


def review_path(run, step):
    return ws(run) / OUT[step]


# ----------------------------------------------------------------------------- briefs (arm-3 branches, strings unchanged)
def ctx_text():
    return (f"First read {D}/README.md (binding shared context; the files under {D}/inventory/ are the only evidence you can check, "
            f"mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file(s).")


def first_review_brief(out):
    spec = SPEC
    head = f"Run /sc:spec-panel @{spec} {FLAGS} ."
    body = f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={spec}."
    return f"{head} {body}\nWrite the full report to {out}. Do not edit anything else. {ctx_text()}"


def gate_brief(out):
    spec = SPEC
    head = f"Run /sc:spec-panel @{spec} {FLAGS} ."
    body = f"Review per the GATE prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={spec}."
    return f"{head} {body}\nWrite the full report to {out}. Do not edit anything else. {ctx_text()}"


def rereview_brief(prior, base, out):
    spec = SPEC
    head = f"Run /sc:spec-panel @{spec} {FLAGS} --re-review {prior} --baseline {base} ."
    body = (f"Re-review per the RE-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. "
            f"Values: candidate={spec}, baseline={base}, prior={prior}.")
    return f"{head} {body}\nWrite the full report to {out}. Do not edit anything else. {ctx_text()}"


def revise_brief(ids, rep, out):
    spec = SPEC
    body = (f"Revise per the REVISE prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. "
            f"Values: candidate={spec}, IDS={ids}.")
    return (f"{body}\nInputs: the review report {rep} (its Reviser brief lists the blocking ids), the spec, and the files under {D}/inventory/. "
            f"Edit the spec {spec} in place; it is the only file you may change besides your output. Do not run the spec-panel. "
            f"Write {out} with the byte accounting the prompt asks for and one row per finding id (applied where, or rejected with a cited reason). {ctx_text()}")


def new_brief(run, step, ids=None):
    if step == "R1":
        return first_review_brief(OUT["R1"])
    if step == "R2":
        return rereview_brief(OUT["R1"], f"{H}/spec-v1.md", OUT["R2"])
    if step == "R3":
        return rereview_brief(OUT["R2"], f"{H}/spec-v2.md", OUT["R3"])
    if step == "G":
        return gate_brief(OUT["G"])
    if step == "GR":
        return rereview_brief(OUT["G"], f"{H}/spec-g.md", OUT["GR"])
    if step in REVISE_STEPS:
        rep = {"V1": OUT["R1"], "V2": OUT["R2"], "GV": OUT["G"]}[step]
        return revise_brief(ids or "the blocking findings listed in the report", rep, OUT[step])
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


def assert_ceiling(st, adding=None):
    """Hard ceiling of the design: at most 5 reviews (R*, G, GR) and 3 fix cycles (V*, GV) per document."""
    done = list(st["done"]) + ([adding] if adding and adding not in st["done"] else [])
    reviews = sum(1 for s in done if re.fullmatch(r"R\d+|G|GR", s))
    revises = sum(1 for s in done if re.fullmatch(r"V\d+|GV", s))
    assert reviews <= 5, f"{st['run']}: ceiling of 5 reviews exceeded ({done})"
    assert revises <= 3, f"{st['run']}: ceiling of 3 fix cycles exceeded ({done})"


def prep_audit(run, k):
    assert k in (1, 2)
    d = run_dir(run)
    name, step = ("aud", "AUD") if k == 1 else ("aud2", "AUD2")
    ad = d / name
    if ad.exists():
        shutil.rmtree(ad)
    (ad / "home/.claude/rules/prompts").mkdir(parents=True)
    shutil.copytree(S1 / "inputs/repo-overlay", ad / "ws")
    (ad / "ws" / D / "review").mkdir(parents=True)
    shutil.copy(ws(run) / SPEC, ad / "ws" / SPEC)
    git_cmd = git_show(BASE_REF, "src/superclaude/commands/spec-panel.md")
    assert hashlib.sha256(git_cmd.encode()).hexdigest() == AUD_CMD_SHA, "frozen audit command hash mismatch"
    rules_txt = (P11 / "rules.md").read_text()
    assert hashlib.sha256(rules_txt.encode()).hexdigest() == AUD_RULES_SHA, "frozen audit rules hash mismatch"
    (ad / "command.md").write_text(git_cmd)
    (ad / "home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules_txt)
    brief = (f"Run /sc:spec-panel @{SPEC} {FLAGS} . This is a labelled whole-document audit of the final spec: a first review of the whole document. "
             f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={SPEC}.\n"
             f"Write the full report to {AUD_OUT}. Do not edit anything else. First read {D}/README.md (binding shared context; the files under {D}/inventory/ "
             f"are the only evidence you can check, mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file.")
    text = WRAP.format(sb=ad, wsdir="ws", cmdpart=CMDPART.format(sb=ad), brief=brief)
    p = d / f"PROMPT-{step}.md"; p.write_text(text)
    return p


def prep_gate(run):
    d = run_dir(run); gd = d / "g"
    if gd.exists():
        shutil.rmtree(gd)
    (gd / "home/.claude/rules/prompts").mkdir(parents=True)
    shutil.copytree(S1 / "inputs/repo-overlay", gd / "ws")
    (gd / "ws" / D / "review").mkdir(parents=True)
    shutil.copy(ws(run) / SPEC, gd / "ws" / SPEC)
    (gd / "command.md").write_text(git_show(PRODUCT_REF, "src/superclaude/commands/spec-panel.md"))
    (gd / "home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(
        git_show(PRODUCT_REF, "src/superclaude/rules/prompts/document_review_loop_prompts.md"))
    text = WRAP.format(sb=gd, wsdir="ws", cmdpart=CMDPART.format(sb=gd), brief=new_brief(run, "G"))
    p = d / "PROMPT-G.md"; p.write_text(text)
    return p


def prep(run, step, subs=None):
    subs = subs or {}
    d = run_dir(run); st = load(run)
    if step in ("AUD", "AUD2"):
        return prep_audit(run, 1 if step == "AUD" else 2)
    assert_ceiling(st, adding=step)
    assert step in LOOP_STEPS, step
    if step == "G":
        return prep_gate(run)
    snap = {"V1": "spec-v1.md", "V2": "spec-v2.md", "GV": "spec-g.md"}.get(step)
    if snap and not (ws(run) / H / snap).exists():
        shutil.copy(ws(run) / SPEC, ws(run) / H / snap)
    ids = None
    if step in REVISE_STEPS:
        rev = {"V1": "R1", "V2": "R2", "GV": "G"}[step]
        ids = subs.get("IDS") or ", ".join(ids_for(run, rev))
        print("IDS =", ids)
    brief = new_brief(run, step, ids)
    cmdpart = CMDPART if step in ("R1", "R2", "R3", "GR") else ""
    text = WRAP.format(sb=d, wsdir="ws", cmdpart=cmdpart.format(sb=d) if cmdpart else "", brief=brief)
    p = d / f"PROMPT-{step}.md"; p.write_text(text)
    return p


# ----------------------------------------------------------------------------- ingest
def out_base(run, step):
    if step == "AUD": return run_dir(run) / "aud" / "ws"
    if step == "AUD2": return run_dir(run) / "aud2" / "ws"
    if step == "G": return run_dir(run) / "g" / "ws"
    return ws(run)


def ingest(run, step):
    st = load(run)
    base = out_base(run, step)
    outp = base / (AUD_OUT if step in ("AUD", "AUD2") else OUT[step])
    rec = {"output_exists": outp.exists(), "stratum": st["stratum"]}
    if outp.exists():
        if step == "G":                         # copy the gate report into the main workspace
            shutil.copy(outp, ws(run) / OUT["G"])
        t = outp.read_text(errors="ignore"); rec["report_bytes"] = len(t.encode())
        if step in REVIEW_STEPS or step in ("AUD", "AUD2"):
            rec["verdict"] = st_.verdict_of(t)
            rec["review_header"] = re.findall(r"^\W*review:\s*(\d)\s*of\s*3", t, re.I | re.M)
            rec["blocking_ids"] = ids_from(outp)
            fs = st_.blocking_findings(outp, ids=st.get("ids", {}).get(step))
            rec["blocking"] = [{"id": f["id"], "theme": f["theme"], "heading": (f["heading"] or "")[:100]} for f in fs]
        if step == "GR":
            rec["header_expected"] = "2"
    if step in ("AUD", "AUD2"):
        rec["spec_audited"] = {"bytes": (base / SPEC).stat().st_size} if (base / SPEC).exists() else {}
    elif step != "G":
        rec["spec_after"] = spec_stats(run)
    st["log"].setdefault(step, {}).update(rec)
    if step not in st["done"]:
        st["done"].append(step)
    assert_ceiling(st)
    save(run, st)
    return rec


# ----------------------------------------------------------------------------- stall check (G)
def stall_check(run):
    gate = ws(run) / OUT["G"]
    st = load(run)
    gs = st_.blocking_findings(gate, ids=st.get("ids", {}).get("G"))
    earlier = []
    for f in ("R1", "R2", "R3"):
        p = ws(run) / OUT[f]
        if p.exists() and f in st["done"]:
            for e in st_.blocking_findings(p, ids=st.get("ids", {}).get(f)):
                earlier.append((f, e))
    pairs = []
    stalled = bool(gs)
    for g in gs:
        hit = next(((f, e) for f, e in earlier if st_.same_defect(g, e)), None)
        if hit is None:
            stalled = False
        else:
            pairs.append([g["id"], pathlib.Path(OUT[hit[0]]).name, hit[1]["id"]])
    return {"auto": stalled, "pairs": pairs, "gate_ids": [g["id"] for g in gs]}


# ----------------------------------------------------------------------------- state machine
def plan(run):
    """Deterministic next step(s) from the ingested state.  Returns dict(next=[...], loop_end=str|None, manual=str|None, complete=bool)."""
    st = load(run)
    done, log = st["done"], st["log"]
    cur = "R1"
    loop_end = None
    while loop_end is None:
        if cur not in done:
            return {"next": [cur], "loop_end": None, "manual": None, "complete": False}
        rec = log[cur]
        if cur in REVISE_STEPS:
            cur = {"V1": "R2", "V2": "R3", "GV": "GR"}[cur]
            continue
        v = rec.get("verdict")
        if v in ("INCOMPLETE", "NONE", None):
            return {"next": [], "loop_end": None, "manual": f"verdict {v}", "complete": False, "kind": "verdict", "at": cur}
        ids = ids_for(run, cur)
        if v == "FAIL" and not ids:
            return {"next": [], "loop_end": None, "manual": "no blocking ids parsed", "complete": False, "kind": "ids", "at": cur}
        if cur in ("R1", "R2"):
            cur = "G" if v == "PASS" else {"R1": "V1", "R2": "V2"}[cur]
        elif cur == "R3":
            if v == "PASS": cur = "G"
            else: loop_end = "ESCALATED"
        elif cur == "G":
            if v == "PASS": loop_end = "GATE-PASS"
            else:
                stall = st.get("stall") or stall_check(run)
                if stall["auto"]: loop_end = "STALLED"
                else: cur = "GV"
        elif cur == "GR":
            loop_end = "GATE-LOOP-PASS" if v == "PASS" else "GATE-LOOP-ESCALATED"
    pend = [s for s in ("AUD", "AUD2") if s not in done]
    return {"next": pend, "loop_end": loop_end, "manual": None, "complete": not pend}


def model_for(run, step):
    if step in ("AUD", "AUD2"):
        return "sonnet"                           # D3: Haiku never audits
    m = load(run)["loop_model"]
    assert m in ("sonnet", "haiku")
    return m


def setids(run, step, text):
    assert step in REVIEW_STEPS, step
    st = load(run)
    st.setdefault("ids", {})[step] = parse_ids(text)
    st["manual"].append({"step": step, "ids": st["ids"][step], "at": now()})
    save(run, st)
    print("ids set", run, step, st["ids"][step])


def unlaunch(run, step):
    st = load(run)
    st["launched"].pop(step, None)
    save(run, st)
    print("unlaunched", run, step)


def lose(run):
    st = load(run); st["lost"] = True; save(run, st); print("lost", run)


def eyeball(run, yn):
    st = load(run)
    assert st.get("stall"), "no stall decision recorded"
    st["stall"]["eyeball"] = (yn == "yes"); save(run, st)


# ----------------------------------------------------------------------------- transcripts / tokens (D2 convention)
def _first_user_text(lines):
    for ln in lines:
        try: d = json.loads(ln)
        except Exception: continue
        if d.get("type") == "user":
            c = (d.get("message") or {}).get("content")
            return c if isinstance(c, str) else json.dumps(c)
    return None


def scan_transcripts(label, run_re):
    """-> {(run, step): [ {file, models, tokens, done} ]}.  A transcript belongs to (run, step) when its first user message
    (which starts with "Read ") names <label>/<run>/PROMPT-<STEP>.md.  Output tokens: sum over unique message.id of the max
    usage.output_tokens (each message id once; a transcript logs a message once per content block)."""
    pat = re.compile(rf"{re.escape(label)}/({run_re})/PROMPT-(\w+)\.md")
    out = {}
    for f in glob.glob(TASKS_GLOB):
        try: lines = open(f, errors="ignore").read().splitlines()
        except Exception: continue
        first = _first_user_text(lines)
        if not first or not first.startswith("Read"):
            continue
        m = pat.search(first[:600])
        if not m:
            continue
        per_id, models, done, start = {}, set(), False, None
        last_text = ""
        for ln in lines:
            try: d = json.loads(ln)
            except Exception: continue
            if start is None and d.get("timestamp"): start = d["timestamp"]
            msg = d.get("message") or {}
            if msg.get("role") != "assistant":
                continue
            if msg.get("model"): models.add(msg["model"])
            u = msg.get("usage") or {}
            mid = msg.get("id") or d.get("uuid")
            per_id[mid] = max(per_id.get(mid, 0), u.get("output_tokens") or 0)
            if isinstance(msg.get("content"), list):
                for c in msg["content"]:
                    if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "SubagentHandback" and "DONE" in json.dumps(c.get("input")):
                        done = True
                    if isinstance(c, dict) and c.get("type") == "text":
                        last_text = c.get("text") or ""
        if "DONE" in last_text:
            done = True
        out.setdefault((m.group(1), m.group(2)), []).append(
            {"file": f, "models": models, "tokens": sum(per_id.values()), "done": done, "start": start})
    return out


def pick(cands, expect_model, key):
    """Keep transcripts whose model matches; if several remain keep the DONE one with the most tokens (WARN)."""
    keep = []
    for c in cands:
        bad = [mm for mm in c["models"] if expect_model not in mm]
        if bad:
            print(f"WARN {key} transcript {os.path.basename(c['file'])} has model {sorted(c['models'])}, expected {expect_model}")
            continue
        keep.append(c)
    if not keep:
        return None
    if len(keep) > 1:
        print(f"WARN {key}: {len(keep)} transcripts; keeping the DONE one with the most tokens")
        keep.sort(key=lambda c: (c["done"], c["tokens"]), reverse=True)
    return keep[0]


def expected_model(run, step):
    return "sonnet" if step in ("AUD", "AUD2") else load(run)["loop_model"]


def run_re_ab(): return r"b3h?-r\d+"


def tokens_cmd():
    sc = scan_transcripts("p12/ab3/runs", run_re_ab())
    for run in all_runs():
        st = load(run)
        for step in STEPS:
            cands = sc.get((run, step))
            if not cands:
                continue
            c = pick(cands, expected_model(run, step), f"{run} {step}")
            if c is None:
                continue
            st["log"].setdefault(step, {})["output_tokens"] = c["tokens"]
        save(run, st)
    print("tokens recorded")


def basetokens(quiet=False):
    sc = scan_transcripts("p11/runs", r"a3-r\d")
    loops, auds = {}, {}
    for (run, step), cands in sorted(sc.items()):
        c = pick(cands, "sonnet", f"{run} {step}")
        if c is None:
            continue
        (auds if step == "AUD" else loops).setdefault(run, 0)
        if step == "AUD": auds[run] += c["tokens"]
        else: loops[run] += c["tokens"]
    if not loops:
        print("no baseline transcripts readable"); return None
    if not quiet:
        for r in sorted(loops): print(r, "loop", loops[r], "audit", auds.get(r))
    lm = sum(loops.values()) / len(loops); am = sum(auds.values()) / max(1, len(auds))
    if not quiet:
        print(f"loop mean {lm:,.0f} (expected 100,424)  audit mean {am:,.0f} (expected 69,044)")
    return {"loop_mean": lm, "audit_mean": am, "loops": loops, "auds": auds}


# ----------------------------------------------------------------------------- status
def status():
    for run in all_runs():
        st = load(run); row = []
        for s in STEPS:
            r = st["log"].get(s)
            if r is None: row.append(f"{s}:-")
            else: row.append(f"{s}:{r.get('verdict', 'ok' if r.get('output_exists') else 'MISSING')}")
        print(run, st["stratum"], " ".join(row), "| loop_end", st.get("loop_end"), "| lost" if st.get("lost") else "")


# ----------------------------------------------------------------------------- analysis (D2, D3, D4, D6 implemented once, here)
def frac(pair): return Fraction(pair[0], pair[1])


def r_loop(loop_tokens_mean, c): return loop_tokens_mean / c["tokens"]["A_BASE"]
def r_b(loop_tokens_mean, aud_tokens_mean, c): return (loop_tokens_mean + aud_tokens_mean) / c["tokens"]["B_BASE"]


def theme_hit(findings): return any(f["theme"] in ("T1", "T2", "T3") for f in findings)


def baseline_stats(c, overrides=None):
    """B_* from the p11 audits plus baseline-audit2 reports when present.  Returns dict with 'provisional'."""
    reports = []
    for k in range(1, 7):
        reports.append(pathlib.Path(c["baseline_runs_dir"]) / f"a3-r{k}/aud/ws/{AUD_OUT}")
    n_second = 0
    for k in range(1, 7):
        p = pathlib.Path(c["baseline_audit2_dir"]) / f"a3-r{k}/ws/{AUD_OUT}"
        if p.exists():
            reports.append(p); n_second += 1
    blk, fails, themes, n = [], 0, 0, 0
    for p in reports:
        if not p.exists():
            continue
        t = p.read_text(errors="ignore"); v = st_.verdict_of(t)
        if v not in ("PASS", "FAIL"):
            continue
        fs = st_.blocking_findings(p, overrides)
        n += 1; blk.append(len(fs)); fails += v == "FAIL"; themes += theme_hit(fs)
    dflt = c["baseline_defaults"]
    if n == 0 or n_second == 0:
        return {"provisional": True, "B_BLK": dflt["B_BLK"], "B_AUDFAIL": frac(dflt["B_AUDFAIL"]), "B_THEME": frac(dflt["B_THEME"]),
                "n_audits": 6, "computed_from_files": {"n": n, "mean_blk": (sum(blk) / n) if n else None}}
    return {"provisional": False, "B_BLK": sum(blk) / n, "B_AUDFAIL": Fraction(fails, n), "B_THEME": Fraction(themes, n), "n_audits": n}


def audit_rows(states, overrides):
    rows = []   # one per audit: run, k, verdict, findings
    for st in states:
        run = st["run"]
        for k, step, sub in ((1, "AUD", "aud"), (2, "AUD2", "aud2")):
            p = run_dir(run) / sub / "ws" / AUD_OUT
            if step not in st["done"] or not p.exists():
                continue
            t = p.read_text(errors="ignore")
            v = st_.verdict_of(t)
            fs = st_.blocking_findings(p, overrides)
            rows.append({"run": run, "k": k, "verdict": v, "findings": fs})
    return rows


def stratum_numbers(states, c, overrides, replica=None):
    """Pure numbers for one stratum.  replica=None pools both audits; 1 or 2 uses that audit only."""
    done = [s for s in states if not s.get("lost") and s.get("loop_end") and "AUD" in s["done"] and "AUD2" in s["done"]]
    rows = [r for r in audit_rows(done, overrides) if replica in (None, r["k"]) and r["verdict"] in ("PASS", "FAIL")]
    n_runs = len(done)
    loop_toks = []
    tok_missing = []
    for s in done:
        tot = 0
        for step in LOOP_STEPS:
            if step in s["done"]:
                t = s["log"][step].get("output_tokens")
                if t is None: tok_missing.append((s["run"], step)); t = 0
                tot += t
        loop_toks.append(tot)
    aud_toks = [s["log"]["AUD"].get("output_tokens") or 0 for s in done]
    loop_mean = sum(loop_toks) / n_runs if n_runs else 0.0
    aud_mean = sum(aud_toks) / n_runs if n_runs else 0.0
    n_aud = len(rows)
    fails = sum(r["verdict"] == "FAIL" for r in rows)
    th = sum(theme_hit(r["findings"]) for r in rows)
    blk = sum(len(r["findings"]) for r in rows)
    final_pass = sum(s["loop_end"] in ("GATE-PASS", "GATE-LOOP-PASS") for s in done)
    scoped_pass = sum(any(s["log"].get(x, {}).get("verdict") == "PASS" for x in ("R1", "R2", "R3")) for s in done)
    growth = [((s["log"]["AUD"].get("spec_audited") or {}).get("bytes", c["SPEC_BYTES"]) - c["SPEC_BYTES"]) / c["SPEC_BYTES"] for s in done]
    scoped_rev = [sum(1 for x in ("R1", "R2", "R3") if x in s["done"]) for s in done]
    gate_rev = [sum(1 for x in ("G", "GR") if x in s["done"]) for s in done]
    return {"n_runs": n_runs, "n_audits": n_aud, "audit_fails": fails, "theme_audits": th,
            "BLK": (blk / n_aud) if n_aud else None, "final_pass": final_pass, "scoped_pass": scoped_pass,
            "LOOP": loop_mean, "AUD": aud_mean, "TOK": loop_mean + aud_mean,
            "R_LOOP": r_loop(loop_mean, c), "R_B": r_b(loop_mean, aud_mean, c),
            "growth": (sum(growth) / n_runs) if n_runs else None,
            "scoped_reviews": scoped_rev, "gate_reviews": gate_rev, "max_reviews": max([a + b for a, b in zip(scoped_rev, gate_rev)] or [0]),
            "tokens_missing": tok_missing}


def decide(num, c, base, n_planned):
    """DROP-1, DROP-2, DROP-3 (post-hoc cost clause, D6), ADOPT, else INCONCLUSIVE.  Returns (outcome, rule, details)."""
    r = c["rules"]
    minc = c["min_completed_sonnet"].get(str(n_planned), c["min_completed_sonnet"]["6"])
    if num["n_runs"] < minc:
        return "INCONCLUSIVE", f"fewer than {minc} completed runs ({num['n_runs']})", {}
    if num["n_audits"] == 0:
        return "INCONCLUSIVE", "no completed audits", {}
    if Fraction(num["theme_audits"], num["n_audits"]) >= frac(r["DROP1_theme_rate_min"]):
        return "DROP", "DROP-1 (gate misses the themes)", {}
    if Fraction(num["final_pass"], num["n_runs"]) < frac(r["DROP2_final_pass_rate_min"]):
        return "DROP", "DROP-2 (non-convergence)", {}
    if num["R_LOOP"] > r["DROP3_r_loop_max"]["value"]:
        return "DROP", f"DROP-3 (cost: R_LOOP {num['R_LOOP']:.2f} > {r['DROP3_r_loop_max']['value']})", {}
    blk_ok = num["BLK"] <= r["ADOPT_blk_factor"] * base["B_BLK"] + 1e-9
    fail_ok = Fraction(num["audit_fails"], num["n_audits"]) <= Fraction(str(r["ADOPT_audfail_factor"])) * base["B_AUDFAIL"]
    if blk_ok and fail_ok:
        return "ADOPT", "ADOPT", {}
    return "INCONCLUSIVE", "no DROP and no ADOPT", {"blk_ok": blk_ok, "fail_ok": fail_ok}


def load_overrides():
    p = AB / "theme-overrides.json"
    return json.load(open(p)) if p.exists() else {}


def haiku_baseline(c):
    """Shared Haiku baseline.  Tolerant of the unknown results.json schema; None when absent or unrecognised."""
    p = pathlib.Path(c["haiku_baseline_path"])
    if not p.exists():
        return None
    try:
        j = json.load(open(p))
    except Exception:
        return None
    out = {"path": str(p), "differences": []}
    runs = j.get("runs") if isinstance(j.get("runs"), dict) else (j if all(isinstance(v, dict) for v in j.values()) else {})
    blk, loops, fails = [], [], 0
    for name, r in runs.items():
        if not isinstance(r, dict): continue
        for key in ("audit_blocking", "blocking_per_audit", "blocking_counts", "n_blocking_audits"):
            if isinstance(r.get(key), list): blk += [int(x) for x in r[key]]; break
        for key in ("loop_tokens", "LOOP", "loop_output_tokens"):
            if isinstance(r.get(key), (int, float)): loops.append(float(r[key])); break
        fails += int(bool(r.get("harness_failure") or r.get("lost") or r.get("manual")))
    # rescore from reports when they exist beside the runs
    rescored = []
    for k in range(1, 7):
        for sub in ("aud", "aud2"):
            rp = p.parent / f"runs/a3-r{k}/{sub}/ws/{AUD_OUT}"
            if rp.exists():
                rescored.append(len(st_.blocking_findings(rp)))
    if rescored:
        if blk and abs(sum(blk) / len(blk) - sum(rescored) / len(rescored)) > 1e-9:
            out["differences"].append(f"H_BLK file {sum(blk)/len(blk):.2f} vs rescored {sum(rescored)/len(rescored):.2f}")
        blk = rescored
    if "H_BLK" in j and not blk: blk = [j["H_BLK"]]
    if "H_LOOP" in j and not loops: loops = [j["H_LOOP"]]
    if not blk or not loops:
        return None
    out.update({"H_BLK": sum(blk) / len(blk), "H_LOOP": sum(loops) / len(loops),
                "harness_failure_rate": Fraction(fails, max(1, len(runs)))})
    return out


def analyze(write=True):
    c = cfg(); ov = load_overrides()
    states = [load(r) for r in all_runs()]
    by = {"sonnet": [s for s in states if s["stratum"] == "sonnet"], "haiku": [s for s in states if s["stratum"] == "haiku"]}
    base = baseline_stats(c, ov)
    out = {"baseline": {"B_BLK": base["B_BLK"], "B_AUDFAIL": str(base["B_AUDFAIL"]), "B_THEME": str(base["B_THEME"]),
                        "provisional": base["provisional"], "n_audits": base["n_audits"]}}
    # Sonnet stratum -----------------------------------------------------------------------
    sn = by["sonnet"]
    n_planned = len(sn)
    num = stratum_numbers(sn, c, ov)
    outcome, rule, det = decide(num, c, base, n_planned)
    reps = {}
    for k in (1, 2):
        nk = stratum_numbers(sn, c, ov, replica=k)
        reps[k] = decide(nk, c, base, n_planned)[0]
    agree = reps[1] == reps[2]
    sonnet_outcome = outcome if agree else "INCONCLUSIVE"
    note = rule if agree else f"replicas disagree (audit 1 {reps[1]}, audit 2 {reps[2]}); pooled rule was: {rule}"
    # Haiku stratum -------------------------------------------------------------------------
    hs = by["haiku"]
    hb = haiku_baseline(c)
    hnum = stratum_numbers(hs, c, ov) if hs else None
    hres = None
    if hnum and hnum["n_runs"] and hb:
        HR = hnum["BLK"] / hb["H_BLK"] if hb["H_BLK"] else None
        fail_rate = Fraction(sum(1 for s in hs if s.get("lost") or s["manual"] or any(v.get("retried") for v in s["log"].values())), len(hs))
        hres = {"H_BLK": hb["H_BLK"], "BLK_TH": hnum["BLK"], "HR": HR, "reduction": (1 - HR) if HR is not None else None,
                "H_LOOP": hb["H_LOOP"], "R_LOOP_H": hnum["LOOP"] / hb["H_LOOP"], "harness_failure_rate": str(fail_rate),
                "baseline_failure_rate": str(hb["harness_failure_rate"]), "differences": hb["differences"]}
        hres["agrees"] = bool(HR is not None and (1 - HR) > 0 and fail_rate <= hb["harness_failure_rate"] + frac(c["haiku_condition"]["max_harness_failure_excess"]))
    final = sonnet_outcome
    if sonnet_outcome == "ADOPT":
        if hres is None:
            final = "ADOPT (Haiku robustness pending)"
        elif not hres["agrees"]:
            final = "INCONCLUSIVE"; note += "; Haiku stratum disagrees"
    out["sonnet"] = {"stratum": "sonnet", "n_planned": n_planned, "numbers": num, "pooled_outcome": outcome, "pooled_rule": rule,
                     "replica_outcomes": {"audit1": reps[1], "audit2": reps[2]}, "sonnet_outcome": sonnet_outcome, "final_outcome": final,
                     "note": note, "provisional": base["provisional"]}
    out["haiku"] = {"stratum": "haiku", "numbers": hnum, "result": hres, "baseline_found": hb is not None}
    if write:
        json.dump(out, open(AB / "metrics.json", "w"), indent=1, default=str)
        (AB / "RESULTS-tables.md").write_text(render_tables(out, sn, hs, ov, c))
    return out


def render_tables(out, sn, hs, ov, c):
    s = out["sonnet"]; n = s["numbers"]; b = out["baseline"]
    lines = [f"# RESULTS tables (generated by harness.py analyze){' - PROVISIONAL (single baseline audit)' if b['provisional'] else ''}", "",
             f"Outcome: **{s['final_outcome']}** ({s['note']})", "",
             f"R_LOOP (decides) = {n['R_LOOP']:.3f}   R_B (reported, never decides) = {n['R_B']:.3f}", "",
             "| Metric | Value |", "|---|---|"]
    for k in ("n_runs", "n_audits", "final_pass", "scoped_pass", "audit_fails", "theme_audits", "BLK", "LOOP", "AUD", "TOK", "growth", "max_reviews"):
        lines.append(f"| {k} | {n[k]} |")
    lines += ["", "## Per run", "", "| run | stratum | loop_end | scoped | gate | G blocking | stall auto/eyeball | AUD | AUD2 |", "|---|---|---|---|---|---|---|---|---|"]
    for st in sn + hs:
        g = st["log"].get("G", {})
        stl = st.get("stall") or {}
        a1 = st["log"].get("AUD", {}); a2 = st["log"].get("AUD2", {})
        f = lambda a: f"{a.get('verdict')} {[(x['id'], x['theme']) for x in a.get('blocking', [])]}"
        lines.append(f"| {st['run']} | {st['stratum']} | {st.get('loop_end')} | {[x for x in ('R1','R2','R3') if x in st['done']]} | "
                     f"{[x for x in ('G','GV','GR') if x in st['done']]} | {[(x['id'], x['theme']) for x in g.get('blocking', [])]} | "
                     f"{stl.get('auto')}/{stl.get('eyeball')} | {f(a1)} | {f(a2)} |")
    lines += ["", "## Tagged findings to eyeball (audits)", ""]
    for r in audit_rows(sn + hs, ov):
        for f_ in r["findings"]:
            lines.append(f"- {r['run']} audit{r['k']} {f_['id']} -> {f_['theme']}: {(f_['heading'] or '')[:100]}")
    if ov:
        lines += ["", "## Theme overrides applied", ""] + [f"- {k}: {v}" for k, v in ov.items()]
    lines += ["", "Circularity: the gate verdict is never an outcome; only AUD and AUD2 decide.", ""]
    return "\n".join(lines)


# ----------------------------------------------------------------------------- CLI
def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    c = a[0]
    if c == "build":
        stratum = a[a.index("--stratum") + 1] if "--stratum" in a else "sonnet"
        build(stratum, "--extend" in a)
    elif c == "prep": print(prep(a[1], a[2], dict(kv.split("=", 1) for kv in a[3:])))
    elif c == "ingest": print(json.dumps({a[1]: {a[2]: ingest(a[1], a[2])}}, indent=1))
    elif c == "setids": setids(a[1], a[2], a[3])
    elif c == "unlaunch": unlaunch(a[1], a[2])
    elif c == "lose": lose(a[1])
    elif c == "eyeball": eyeball(a[1], a[2])
    elif c == "status": status()
    elif c == "tokens": tokens_cmd()
    elif c == "basetokens": basetokens()
    elif c == "analyze": print(json.dumps(analyze(), indent=1, default=str))
    else: sys.exit(__doc__)


if __name__ == "__main__":
    main()
