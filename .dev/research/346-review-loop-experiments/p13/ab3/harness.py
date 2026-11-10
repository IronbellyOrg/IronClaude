#!/usr/bin/env python3
"""PN3 harness for arm c3 (capture-recapture stop rule over a four-reviewer panel).  Usage:
  harness.py build [--stratum sonnet|haiku] [N]   create N fresh runs (sonnet: c3-r<i>, haiku: c3-h<i>)
  harness.py prep RUN STEP                        write RUN/PROMPT-STEP.md (STEP: P<n>.<rid> V<r> R<r+1> AUD AUD2)
  harness.py ingest RUN STEP | progress RUN       record outputs / move the state machine forward
  harness.py status | basetokens | analyze | extend | gate
The frozen pieces below (S1, D, SPEC, FLAGS, AUD_OUT, section, git_show, new_brief, WRAP, CMDPART) are copied byte for byte
from $SP/p11/harness.py (Stage 2); tests/test_ab3.py pins prompt identity against the p11 prompts."""
import json, re, sys, shutil, hashlib, subprocess, pathlib, collections, os
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ledger_lite as L, panel_lite as PL, tokens as TK, telemetry_lite as TL, decision as DEC
S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S/"scratchpad"; P11 = SP/"p11"; AB = SP/"p13"/"ab3"; RUNS = AB/"runs"; TASKS = S/"tasks"
S1 = SP/"exp346/.dev/experiments/346-validation/phase2/S1"
REPO = str(SP/"p13"/"clones"/"pn3")
BASE_REF = "69ac8b3335564fb5551980e984c5d9b763039cc1"
AUD_CMD_SHA = "e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494"
AUD_RULES_SHA = "3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8"
SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
DESIGN = "c3"
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
OUT = {3: {"R1": f"{D}/review/round1.md", "V1": f"{D}/review/revise1.md", "R2": f"{D}/review/round2.md",
           "V2": f"{D}/review/revise2.md", "R3": f"{D}/review/round3.md"}}
AUD_OUT = f"{D}/review/audit.md"
FLAGS = "--mode critique --focus requirements,architecture"
def git_show(ref, path): return subprocess.run(["git","-C",REPO,"show",f"{ref}:{path}"],check=True,capture_output=True,text=True).stdout
def arm_of(run): return 3
def section(text, title):
    m = re.search(rf"^### {re.escape(title)}\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    return m.group(1).strip()

def new_brief(run, step, ids):
    a = arm_of(run); rules = (P11/"rules.md").read_text()
    spec = SPEC; H = f"{D}/specs/history"
    def prompt_text(title, vals):
        s = section(rules, title)
        for k, v in vals.items(): s = s.replace("{{%s}}" % k, v)
        return s
    ctx = (f"First read {D}/README.md (binding shared context; the files under {D}/inventory/ are the only evidence you can check, "
           f"mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file(s).")
    if step == "R1":
        out = OUT[a]["R1"]
        head = f"Run /sc:spec-panel @{spec} {FLAGS} ."
        if a == 3: body = (f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={spec}.")
        else: body = "Follow this review prompt:\n" + prompt_text("FIRST-REVIEW prompt", {"CANDIDATE": spec})
        return f"{head} {body}\nWrite the full report to {out}. Do not edit anything else. {ctx}"
    if step in ("R2", "R3"):
        n = 2 if step == "R2" else 3
        prior = OUT[a]["R1" if n == 2 else "R2"]; base = f"{H}/spec-v{n-1}.md"
        head = f"Run /sc:spec-panel @{spec} {FLAGS} --re-review {prior} --baseline {base} ."
        vals = {"CANDIDATE": spec, "BASELINE": base, "PRIOR": prior, "N": str(n)}
        if a == 3: body = (f"Re-review per the RE-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. "
                           f"Values: candidate={spec}, baseline={base}, prior={prior}.")
        else: body = "Follow this re-review prompt:\n" + prompt_text("RE-REVIEW prompt", vals)
        return f"{head} {body}\nWrite the full report to {OUT[a][step]}. Do not edit anything else. {ctx}"
    if step in ("V1", "V2"):
        n = 1 if step == "V1" else 2; rep = OUT[a]["R1" if n == 1 else "R2"]
        vals = {"CANDIDATE": spec, "IDS": ids or "the blocking findings listed in the report"}
        if a == 3: body = (f"Revise per the REVISE prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. "
                           f"Values: candidate={spec}, IDS={vals['IDS']}.")
        else: body = "Follow this revise prompt:\n" + prompt_text("REVISE prompt", vals)
        return (f"{body}\nInputs: the review report {rep} (its Reviser brief lists the blocking ids), the spec, and the files under {D}/inventory/. "
                f"Edit the spec {spec} in place; it is the only file you may change besides your output. Do not run the spec-panel. "
                f"Write {OUT[a][step]} with the byte accounting the prompt asks for and one row per finding id (applied where, or rejected with a cited reason). {ctx}")
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


# ====================================================================== PN3 additions (everything above is frozen)
RULES = DEC.RULES
PANEL_IDS = ["t1b-1", "t2-1", "t3-1", "t3-2"]
CAP = RULES["panel"]["cap_reviews"]
TASK_RE = r"p13/ab3/runs/(?P<run>c3-[rh]\d+)/PROMPT-(?P<step>[\w.\-]+)\.md"
ESTIMATE_FN = None   # tests inject a callable(capture_obj, open_blocking) -> dict


def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def run_dir(run): return RUNS/run
def load(run): return json.load(open(run_dir(run)/"state.json"))
def save(run, st):
    tmp = run_dir(run)/"state.json.tmp"; json.dump(st, open(tmp, "w"), indent=1); os.replace(tmp, run_dir(run)/"state.json")
def ws(run): return run_dir(run)/"ws"
def stratum_of(run): return "haiku" if run.startswith("c3-h") else "sonnet"
def rep_of(run): return int(run.split("-")[1][1:])
def spec_stats(base):
    b = pathlib.Path(base).read_bytes(); return {"bytes": len(b), "lines": b.count(b"\n"), "sha256": hashlib.sha256(b).hexdigest()}


# ---- C4.3 rules text (experiment copies only; never committed to the product)
INS_A = '- **Findings block**: end the report with the findings block described under "Findings block" below, one line per finding, blocking or not.'
INS_B = '- **Findings block**: end the report with the findings block described under "Findings block" below: one line per finding you report and one prior line per prior blocking finding.'
INS_C = '- **Fix map**: end your output with the fix map described under "Fix map" below.'
INS_D = '''### Findings block

The last section of every review report is `## Findings block`: one fenced code block whose info string is `findings-v1`, holding one JSON object per line and nothing else. A report with no finding has an empty block.

- Finding line: `{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "<text copied exactly from the candidate>", "anchor2": "<optional second exact quote>", "refs": ["AC-0.4"], "claim": "<one sentence naming the wrong outcome>"}`. `severity` is CRITICAL, MAJOR or MINOR. `blocking` is true only for a finding that passes the grading check. `category` is one of contradiction, unpassable-check, data-loss, safety, missing-requirement, other. `anchor` is 12 to 200 characters copied exactly from the candidate: the text that is wrong; for a contradiction `anchor2` is the other side. `refs` lists the requirement ids and section numbers the finding rests on.
- Prior line, re-reviews only: `{"prior": "L3", "status": "resolved"}`, with status resolved, open or regressed, one line per prior blocking finding id.
- The block restates the findings discussed above it and adds none. The verdict line stays the reviewer's verdict.

### Fix map

The reviser ends its output with `## Fix map`: one fenced code block whose info string is `fixmap-v1`, one JSON object per line, `{"id": "L3", "action": "applied", "reason": "<one sentence>"}`, with action applied or rejected, one line per blocking id in the brief.
'''


def apply_c43(text):
    """Insert C4.3 Insertions A-D into the base rules text; every anchor must occur exactly once."""
    lines = text.split("\n")
    def only(pred, what):
        idx = [i for i, l in enumerate(lines) if pred(l)]
        assert len(idx) == 1, f"anchor for {what}: expected exactly one line, found {len(idx)}"
        return idx[0]
    ia = only(lambda l: l.startswith('- First-review brief: "'), "A")
    ib = only(lambda l: l.startswith('- Re-review brief: "'), "B")
    ic = only(lambda l: l.startswith('- Revise brief: "'), "C")
    idn = only(lambda l: l == "## Never", "D")
    out = []
    for i, l in enumerate(lines):
        if i == idn:
            out += INS_D.rstrip("\n").split("\n") + [""]
        out.append(l)
        if i == ia: out.append(INS_A)
        if i == ib: out.append(INS_B)
        if i == ic: out.append(INS_C)
    return "\n".join(out)


def base_rules():
    t = (P11/"rules.md").read_text()
    assert hashlib.sha256(t.encode()).hexdigest() == AUD_RULES_SHA, "rules.md sha mismatch"
    return t


def c3_rules(): return apply_c43(base_rules())


def cmd_text():
    t = git_show(BASE_REF, "src/superclaude/commands/spec-panel.md")
    assert hashlib.sha256(t.encode()).hexdigest() == AUD_CMD_SHA, "command sha mismatch"
    return t


def seed_sandbox(sb, spec_text=None, with_history=False, rules=None):
    sb = pathlib.Path(sb)
    (sb/"home/.claude/rules/prompts").mkdir(parents=True)
    shutil.copytree(S1/"inputs/repo-overlay", sb/"ws")
    (sb/"ws"/D/"review").mkdir(parents=True)
    if with_history: (sb/"ws"/D/"specs/history").mkdir(parents=True)
    if spec_text is not None: (sb/"ws"/SPEC).write_text(spec_text)
    (sb/"command.md").write_text(cmd_text())
    (sb/"home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules if rules is not None else c3_rules())


def build(n, stratum="sonnet", start=1):
    pre = "c3-h" if stratum == "haiku" else "c3-r"
    made = []
    for i in range(start, start + n):
        run = f"{pre}{i}"; d = run_dir(run)
        if d.exists(): print("skip existing", run); continue
        seed_sandbox(d, with_history=True)
        res = PL.resolve(PL.PANEL, PL.TIERS, RULES["panel"]["environment"], run)
        save(run, {"run": run, "arm": 3, "design": DESIGN, "stratum": stratum, "rep": i, "done": [], "log": {}, "panel": res,
                   "cursor": {"kind": "panel", "n": 1}, "reviews": 0, "revisions": 0, "panel_rounds": [], "decision": None,
                   "events": [], "extension": i > RULES["sonnet"]["n"] and stratum == "sonnet"})
        L.Ledger(doc=SPEC, cap=CAP).save(d/"ledger.json")
        made.append(run)
    print("built", made); return made


# ---- models and steps
def model_for(run, step):
    st = load(run)
    if step in ("AUD", "AUD2"): return RULES["haiku"]["audit_model"]          # D3: audits always Sonnet
    if re.match(r"P\d+\.", step):
        rid = step.split(".", 1)[1]
        return next(r["launch"] for r in st["panel"]["reviewers"] if r["reviewer_id"] == rid)   # panel composition unchanged by stratum
    return "haiku" if st["stratum"] == "haiku" else "sonnet"                    # D3: non-panel loop workers drop to Haiku


def panel_steps(n): return [f"P{n}.{rid}" for rid in PANEL_IDS]
def step_sandbox(run, step):
    if step in ("AUD", "AUD2"): return run_dir(run)/step.lower()
    if re.match(r"P\d+\.", step): return run_dir(run)/"panel"/step
    return run_dir(run)


def step_output(run, step):
    sb = step_sandbox(run, step)
    if step in ("AUD", "AUD2"): return sb/"ws"/AUD_OUT
    if re.match(r"P\d+\.", step): return sb/"ws"/OUT[3]["R1"]
    return sb/"ws"/OUT[3][step]


def prep(run, step):
    d = run_dir(run); p = d/f"PROMPT-{step}.md"
    if p.exists(): return p
    st = load(run); sb = step_sandbox(run, step)
    if step in ("AUD", "AUD2"):
        if sb.exists(): shutil.rmtree(sb)
        seed_sandbox(sb, spec_text=(ws(run)/SPEC).read_text(), rules=base_rules())    # frozen audit: unmodified rules file (C9.2)
        brief = (f"Run /sc:spec-panel @{SPEC} {FLAGS} . This is a labelled whole-document audit of the final spec: a first review of the whole document. "
                 f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={SPEC}.\n"
                 f"Write the full report to {AUD_OUT}. Do not edit anything else. First read {D}/README.md (binding shared context; the files under {D}/inventory/ "
                 f"are the only evidence you can check, mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file.")
        cmdpart = CMDPART
    elif re.match(r"P\d+\.", step):
        if sb.exists(): shutil.rmtree(sb)
        seed_sandbox(sb, spec_text=(ws(run)/SPEC).read_text())
        brief, cmdpart = new_brief(run, "R1", None), CMDPART
    else:
        if step in ("V1", "V2"):
            shutil.copy(ws(run)/SPEC, ws(run)/D/"specs/history"/f"spec-v{step[1]}.md")
            ids = ", ".join(open_ids(run)); print("IDS =", ids)
            brief = new_brief(run, step, ids); cmdpart = ""
        else:
            brief, cmdpart = new_brief(run, step, None), CMDPART
    text = WRAP.format(sb=sb, wsdir="ws", cmdpart=cmdpart.format(sb=sb) if cmdpart else "", brief=brief)
    p.write_text(text); return p


def ledger(run): return L.Ledger.load(run_dir(run)/"ledger.json")
def open_ids(run): return ledger(run).open_blocking()


# ---- merged report written for the reviser and the next re-review (the prior)
REVISER_RULES = """Rules (restating `command.md:263`):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size before and after, with the bytes added and deleted per finding id.
- Leave Medium and minor findings alone, including through any "apply all findings" wording.
- Return the candidate once and do not award yourself a PASS."""


def merged_report(run, n, lg, info, raw_texts):
    rows = [r for r in lg.rows if r["blocking"] and r["status"] in ("open", "regressed")]
    out = [f"review: {n} of {CAP}", "", f"# Merged review report, round {n} ({info['findings']} findings in {info['clusters']} clusters)", "",
           "Each row below is one defect (a cluster of the reviewers' findings). The ids are ledger ids.", "",
           "| id | status | severity | category | confidence | reviewers | anchor |", "|---|---|---|---|---|---|---|"]
    for r in lg.rows:
        who = sorted({m["reviewer_id"] for m in r["members"] if m["round"] == n})
        out.append(f"| {r['lid']} | {r['status']} | {r['severity_max']} | {r['category']} | {r['confidence']} | {', '.join(who) or '-'} | {' '.join((r['anchor'] or '').split())[:140].replace('|', '/')} |")
    out += ["", "## Claims", ""]
    for lid, claims in info.get("claims", {}).items():
        out.append(f"- {lid}: " + " / ".join(dict.fromkeys(c for c in claims if c)))
    out += ["", "## Reviser brief", "",
            f"Blocking finding ids to repair, and only these: **{', '.join(r['lid'] for r in rows) or 'none'}**. The reviser reads this report, not the command. " + REVISER_RULES,
            "", f"verdict: {'FAIL' if rows else 'PASS'}", "", "## Reviewer reports (verbatim)", ""]
    for rid, t in raw_texts:
        out += [f"### {rid}", "", t, ""]
    return "\n".join(out)


def estimate(capture_obj, open_blocking, blocking_only=True):
    if ESTIMATE_FN: return ESTIMATE_FN(capture_obj, open_blocking)
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh: json.dump(capture_obj, fh); name = fh.name
    cmd = ["uv", "run", "--project", REPO, "superclaude", "review", "estimate", name, "--open-blocking", str(open_blocking)]
    if blocking_only: cmd.append("--blocking-only")
    r = subprocess.run(cmd, capture_output=True, text=True); os.unlink(name)
    if r.returncode != 0: raise RuntimeError(f"estimate failed: {r.stderr}")
    return json.loads(r.stdout)


def event(st, kind, **kw): st["events"].append({"kind": kind, **kw})
def read_text(p): return pathlib.Path(p).read_text(errors="ignore")


def finish(st, decision):
    st["decision"] = decision; st["cursor"] = {"kind": "audit"}; event(st, "decision", decision=decision, reviews=st["reviews"])


def after_review(run, st, lg, n, whole):
    """Cursor logic after review n has been merged (whole = it was a whole-document panel round)."""
    cap_hit = n >= CAP
    if lg.verdict() == "FAIL":
        if cap_hit: finish(st, "ESCALATE"); return
        st["cursor"] = {"kind": "revise", "r": st["revisions"] + 1}; return
    # PASS: the capture-recapture stop rule decides, from the latest whole-document panel round
    cap_obj = json.load(open(run_dir(run)/"capture.json"))
    est = estimate(cap_obj, 0)
    event(st, "stop_rule", review=n, stop=est["stop"], unseen_upper95=est["unseen_upper95"], S_obs=est["S_obs"], reason=est["reason"])
    if est["stop"]: finish(st, "PASS")
    elif cap_hit: finish(st, "ESCALATE")
    else: st["cursor"] = {"kind": "panel", "n": n + 1}


def progress(run):
    """Move the run forward as far as finished steps allow. Returns the list of steps now ready to launch."""
    st = load(run); lg = ledger(run)
    while True:
        cur = st["cursor"]; k = cur["kind"]
        if k == "panel":
            n = cur["n"]; steps = panel_steps(n)
            if not all(s in st["done"] for s in steps):
                for s in steps:
                    if s not in st["done"]: prep(run, s)
                save(run, st); return [s for s in steps if s not in st["done"]]
            doc = read_text(ws(run)/SPEC); revs, raws = [], []
            for rid in PANEL_IDS:
                t = read_text(step_output(run, f"P{n}.{rid}")) if step_output(run, f"P{n}.{rid}").exists() else ""
                m = next(r for r in st["panel"]["reviewers"] if r["reviewer_id"] == rid)
                revs.append({"reviewer_id": rid, "model": m["model"], "report": str(step_output(run, f"P{n}.{rid}")), "text": t}); raws.append((rid, t))
            info = lg.add_round(n, doc, revs)
            info["claims"] = round_claims(lg, n, revs, doc)
            r = st["revisions"]
            (ws(run)/OUT[3][f"R{r + 1}"]).write_text(merged_report(run, n, lg, info, raws))
            cap_obj = lg.capture(n, str(run_dir(run)/"ledger.json")); json.dump(cap_obj, open(run_dir(run)/"capture.json", "w"))
            est = estimate(cap_obj, len(lg.open_blocking()))
            event(st, "panel_round", review=n, S_obs=est["S_obs"], unseen_upper95=est["unseen_upper95"], stop=est["stop"], open_blocking=len(lg.open_blocking()),
                  block_ok=[x["block_ok"] for x in lg.d["rounds"][-1]["reviewers"]])
            st["reviews"] = n; st["panel_rounds"].append(n); lg.save(run_dir(run)/"ledger.json")
            after_review(run, st, lg, n, True)
        elif k == "revise":
            r = cur["r"]; s = f"V{r}"
            if s not in st["done"]:
                prep(run, s); save(run, st); return [s]
            old = read_text(ws(run)/D/"specs/history"/f"spec-v{r}.md"); new = read_text(ws(run)/SPEC)
            fm = L.parse_fixmap(read_text(ws(run)/OUT[3][s]) if (ws(run)/OUT[3][s]).exists() else "")
            lg.apply_revision(old, new, fm["items"]); lg.save(run_dir(run)/"ledger.json")
            event(st, "revision", r=r, fixmap_ok=fm["ok"], items=len(fm["items"]), bytes=len(new.encode()))
            st["revisions"] = r; st["cursor"] = {"kind": "rereview", "r": r}
        elif k == "rereview":
            r = cur["r"]; s = f"R{r + 1}"
            if s not in st["done"]:
                prep(run, s); save(run, st); return [s]
            n = st["reviews"] + 1
            doc = read_text(ws(run)/SPEC); out = ws(run)/OUT[3][s]
            raw = read_text(out) if out.exists() else ""
            m = {"reviewer_id": "rr-1", "model": model_for(run, s), "report": str(out), "text": raw}
            info = lg.add_round(n, doc, [m]); info["claims"] = round_claims(lg, n, [m], doc)
            (ws(run)/D/"review"/f"raw-{s}.md").write_text(raw)
            out.write_text(merged_report(run, n, lg, info, [("rr-1", raw)]))
            event(st, "rereview", review=n, open_blocking=len(lg.open_blocking()), block_ok=lg.d["rounds"][-1]["reviewers"][0]["block_ok"])
            st["reviews"] = n; lg.save(run_dir(run)/"ledger.json")
            after_review(run, st, lg, n, False)
        elif k == "audit":
            need = [s for s in ("AUD", "AUD2") if s not in st["done"]]
            for s in need: prep(run, s)
            if need: save(run, st); return need
            st["cursor"] = {"kind": "done"}
        else:
            save(run, st); return []


def round_claims(lg, n, revs, doc):
    """lid -> claims of this round's findings (re-derived the same way add_round clustered them)."""
    out = {}
    for r in lg.rows:
        for m in r["members"]:
            if m["round"] != n: continue
            rv = next((x for x in revs if x["reviewer_id"] == m["reviewer_id"]), None)
            if not rv: continue
            for f in L.parse_block(rv["text"])["findings"]:
                if f["id"] == m["fid"]: out.setdefault(r["lid"], []).append(f.get("claim", ""))
    return out


def ingest(run, step):
    st = load(run); out = step_output(run, step)
    rec = {"output_exists": out.exists()}
    if out.exists():
        t = out.read_text(errors="ignore"); rec["report_bytes"] = len(t.encode())
        vs = re.findall(r"verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)", t, re.I); rec["verdict"] = vs[-1].upper() if vs else "NONE"
        if step in ("AUD", "AUD2"):
            rec["blocking_ids"] = TK_ids(out); rec["blocking_list"] = parse_ids_c93(out, rec["verdict"])
        if re.match(r"P\d+\.", step):
            rec["block_ok"] = L.parse_block(t)["ok"]
            (ws(run)/D/"review"/"panel").mkdir(parents=True, exist_ok=True); (ws(run)/D/"review"/"panel"/f"{step}.md").write_text(t)
    if step.startswith(("V", "R")): rec["spec_after"] = spec_stats(ws(run)/SPEC)
    st["log"][step] = rec
    if step not in st["done"]: st["done"].append(step)
    save(run, st); return rec


# ---- C9.3 parsing for audits (same functions as the PN3 offline phase)
def _c93():
    sys.path.insert(0, str(AB/"offline")); import common as c; return c
def TK_ids(path): return _c93().ids_from(path)
def parse_ids_c93(path, verdict):
    c = _c93(); return c.parse_ids(c.ids_from(path)) if verdict == "FAIL" else []


# ---- tokens (C9.1) and results
def step_tokens(run=None):
    allt = TK.step_tokens(TASK_RE, None, warn=lambda m: print(m, file=sys.stderr))
    return {k: v for k, v in allt.items() if run is None or k[0] == run}


def run_result(run, toks=None):
    st = load(run); toks = toks if toks is not None else step_tokens(run)
    loop = sum(v for (r, s), v in toks.items() if r == run and s not in ("AUD", "AUD2"))
    aud = toks.get((run, "AUD"))
    blk = [len(st["log"][s].get("blocking_list", [])) for s in ("AUD", "AUD2") if s in st["log"]]
    completed = st["cursor"]["kind"] == "done" and len(blk) == 2
    spec_bytes = spec_stats(ws(run)/SPEC)["bytes"]; base = 57763
    return {"run": run, "stratum": st["stratum"], "completed": completed, "decision": st["decision"], "reviews": st["reviews"],
            "panel_rounds": list(st["panel_rounds"]), "growth_pct": (spec_bytes - base) / base * 100, "loop_tokens": loop or None,
            "audit_tokens": aud, "blk": blk, "failed": bool(st.get("lost")),
            "stops": [e for e in st["events"] if e["kind"] == "stop_rule"]}


def basetokens():
    r = TK.step_tokens(r"p11/runs/(?P<run>a\d-r\d)/PROMPT-(?P<step>\w+)\.md", "sonnet", warn=lambda m: print(m, file=sys.stderr))
    loop, aud = collections.defaultdict(int), collections.defaultdict(int)
    for (run, step), v in r.items():
        if run.startswith("a3"): (aud if step == "AUD" else loop)[run] += v
    runs = sorted(loop)
    A = sum(loop[x] for x in runs) / len(runs); B = sum(aud[x] for x in runs) / len(runs)
    print("per-run arm-3 loop tokens:", {x: loop[x] for x in runs}); print(f"A_BASE (loop only) = {A:,.0f}   one audit = {B:,.0f}   B_BASE (loop + audit) = {A + B:,.0f}")
    return {"loop": dict(loop), "A_BASE": A, "AUD": B, "B_BASE": A + B}


def status():
    for run in sorted(p.name for p in RUNS.iterdir() if (p/"state.json").exists()):
        st = load(run)
        print(run, st["stratum"], "cursor", st["cursor"], "reviews", st["reviews"], "revisions", st["revisions"], "decision", st["decision"], "done", st["done"])


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "build":
        args = sys.argv[2:]; strat = "sonnet"
        if "--stratum" in args: i = args.index("--stratum"); strat = args[i + 1]; del args[i:i + 2]
        build(int(args[0]) if args else (RULES["sonnet"]["n"] if strat == "sonnet" else RULES["haiku"]["n"]), strat)
    elif c == "prep": print(prep(sys.argv[2], sys.argv[3]))
    elif c == "ingest": print(json.dumps(ingest(sys.argv[2], sys.argv[3]), indent=1))
    elif c == "progress": print(progress(sys.argv[2]))
    elif c == "status": status()
    elif c == "basetokens": basetokens()
    elif c in ("analyze", "extend", "gate"):
        import analyze as AN; getattr(AN, c)()
