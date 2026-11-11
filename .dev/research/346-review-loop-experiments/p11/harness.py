#!/usr/bin/env python3
"""Stage 2 harness: S1 spec review loop, 3 arms.  Usage:
  harness.py build                     create 9 sandboxes
  harness.py prep RUN STEP [K=V ...]   write RUN/PROMPT-STEP.md (STEP in R1 V1 R2 V2 R3 AUD)
  harness.py ingest RUN STEP           record outputs of a finished step
  harness.py status                    table of all runs
  harness.py peek RUN STEP             hints for arm-1 substitutions
Arms: a1 = master command + original briefs; a2 = master command + new prompts pasted inline;
a3 = new command + rules file + pointer briefs.  Audit instrument is identical in every arm."""
import json, re, sys, shutil, hashlib, subprocess, pathlib, collections
S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S/"scratchpad"; P11 = SP/"p11"; RUNS = P11/"runs"; TASKS = S/"tasks"
S1 = SP/"exp346/.dev/experiments/346-validation/phase2/S1"
REPO = "/home/user/IronClaude"
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
STEPS = ["R1", "V1", "R2", "V2", "R3", "AUD"]
OUT = {  # step -> output file relative to ws
 1: {"R1": f"{D}/review/spec-panel.md", "V1": f"{D}/review/disposition.md", "R2": f"{D}/review/spec-panel-round2.md",
     "V2": f"{D}/review/disposition-round2.md", "R3": f"{D}/review/spec-panel-round3.md"},
}
for a in (2, 3):
    OUT[a] = {"R1": f"{D}/review/round1.md", "V1": f"{D}/review/revise1.md", "R2": f"{D}/review/round2.md",
              "V2": f"{D}/review/revise2.md", "R3": f"{D}/review/round3.md"}
AUD_OUT = f"{D}/review/audit.md"
FLAGS = "--mode critique --focus requirements,architecture"

def git_show(ref, path): return subprocess.run(["git","-C",REPO,"show",f"{ref}:{path}"],check=True,capture_output=True,text=True).stdout
def run_dir(run): return RUNS/run
def arm_of(run): return int(run[1])
def load(run): return json.load(open(run_dir(run)/"state.json"))
def save(run, st): json.dump(st, open(run_dir(run)/"state.json","w"), indent=1)
def ws(run): return run_dir(run)/"ws"
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def spec_stats(run, base=None):
    p = (base or ws(run))/SPEC; b = p.read_bytes()
    return {"bytes": len(b), "lines": b.count(b"\n"), "sha256": hashlib.sha256(b).hexdigest()}

def section(text, title):
    m = re.search(rf"^### {re.escape(title)}\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    return m.group(1).strip()

def build(arms=(1, 2, 3), reps=(1, 2, 3)):
    cmd_old = git_show("origin/master", "src/superclaude/commands/spec-panel.md")
    cmd_new = git_show("346Claude-p8a-first-review-grading", "src/superclaude/commands/spec-panel.md")
    rules = git_show("346Claude-p8a-first-review-grading", "src/superclaude/rules/prompts/document_review_loop_prompts.md")
    for a in arms:
        for r in reps:
            run = f"a{a}-r{r}"; d = run_dir(run)
            if d.exists(): print('skip existing', run); continue
            (d/"home/.claude/rules/prompts").mkdir(parents=True)
            shutil.copytree(S1/"inputs/repo-overlay", d/"ws")
            (d/"ws"/D/"review").mkdir(parents=True); (d/"ws"/D/"specs/history").mkdir(parents=True)
            (d/"command.md").write_text(cmd_new if a == 3 else cmd_old)
            if a == 3: (d/"home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules)
            save(run, {"run": run, "arm": a, "rep": r, "done": [], "log": {}})
    (P11/"rules.md").write_text(rules)
    print("built", sorted(p.name for p in RUNS.iterdir()))

def original_brief(step, subs):
    names = {"R1": "T05-R1-reviewer-L11-699ae853.txt", "V1": "T06-R1-reviser-L10-3bb70411.txt"}
    tem = {"R2": "T07-R2-reviewer.TEMPLATE.txt", "V2": "T08-R2-reviser.TEMPLATE.txt", "R3": "T09-R3-reviewer.TEMPLATE.txt"}
    if step in names: t = (S1/"briefs/task-text"/names[step]).read_text()
    else:
        t = (S1/"briefs/templates"/tem[step]).read_text()
        for k, v in subs.items(): t = t.replace("{{%s}}" % k, v)
        assert "{{" not in t, f"unfilled placeholder in {step}: {re.findall(r'{{.*?}}', t)}"
    return t.strip()

def adapt_original(t, run):
    t = re.sub(r"Repo root: [^\n]*?\. First read", "Repo root: the workspace directory (relative paths resolve there). First read", t)
    t, n = re.subn(r"Finish with worker_done --report-path <your (?:output|report) file>\.", "Finish by replying with only DONE and your output file path.", t)
    assert n == 1, "worker_done sentence not found"
    return t

def ids_from(report_path):
    t = pathlib.Path(report_path).read_text(errors="ignore")
    m = re.findall(r"(?im)^\W*(?:\*\*)?(?:Reviser brief\W*)?Blocking (?:finding )?ids?\W*[:\-]\s*(.+)$", t)
    if m: return m[-1].strip(" *.")
    sec = re.search(r"(?ms)^#+\s*Reviser brief[^\n]*\n(.*?)(?=^#+ |^verdict:|\Z)", t)
    if not sec: return None
    para = "\n".join([l for l in sec.group(1).splitlines() if l.strip()][:3])
    toks = []
    for x in re.findall(r"\b(?:R\d-)?[A-Z]{1,2}-?\d+\b", para):
        if x not in toks and not x.startswith(("FR", "AC", "SHA")): toks.append(x)
    return ", ".join(toks) or None

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

def prep(run, step, subs):
    a = arm_of(run); d = run_dir(run); st = load(run)
    if step == "AUD":
        ad = d/"aud"
        if ad.exists(): shutil.rmtree(ad)
        (ad/"home/.claude/rules/prompts").mkdir(parents=True)
        shutil.copytree(S1/"inputs/repo-overlay", ad/"ws")
        (ad/"ws"/D/"review").mkdir(parents=True)
        shutil.copy(ws(run)/SPEC, ad/"ws"/SPEC)
        git_cmd = git_show("346Claude-p8a-first-review-grading", "src/superclaude/commands/spec-panel.md")
        (ad/"command.md").write_text(git_cmd); (ad/"home/.claude/rules/prompts/document_review_loop_prompts.md").write_text((P11/"rules.md").read_text())
        brief = (f"Run /sc:spec-panel @{SPEC} {FLAGS} . This is a labelled whole-document audit of the final spec: a first review of the whole document. "
                 f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={SPEC}.\n"
                 f"Write the full report to {AUD_OUT}. Do not edit anything else. First read {D}/README.md (binding shared context; the files under {D}/inventory/ "
                 f"are the only evidence you can check, mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file.")
        sb, wsdir, cmdpart = ad, "ws", CMDPART
    else:
        if step == "V1": shutil.copy(ws(run)/SPEC, ws(run)/D/"specs/history/spec-v1.md")
        if step == "V2": shutil.copy(ws(run)/SPEC, ws(run)/D/"specs/history/spec-v2.md")
        sb, wsdir = d, "ws"
        if a == 1:
            brief = adapt_original(original_brief(step, subs), run)
        else:
            ids = None
            if step in ("V1", "V2"): ids = subs.get("IDS") or ids_from(ws(run)/OUT[a]["R1" if step == "V1" else "R2"]); print("IDS =", ids)
            brief = new_brief(run, step, ids)
        cmdpart = CMDPART if step in ("R1", "R2", "R3") else ""
    text = WRAP.format(sb=sb, wsdir=wsdir, cmdpart=cmdpart.format(sb=sb) if cmdpart else "", brief=brief)
    p = d/f"PROMPT-{step}.md"; p.write_text(text); print(p)

def ingest(run, step):
    a = arm_of(run); st = load(run)
    base = (run_dir(run)/"aud"/"ws") if step == "AUD" else ws(run)
    outp = base/(AUD_OUT if step == "AUD" else OUT[a][step])
    rec = {"output_exists": outp.exists()}
    if outp.exists():
        t = outp.read_text(errors="ignore"); rec["report_bytes"] = len(t.encode())
        if step in ("R1", "R2", "R3", "AUD"):
            vs = re.findall(r"verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)", t, re.I); rec["verdict"] = vs[-1].upper() if vs else "NONE"
            hdr = re.findall(r"^\W*review:\s*(\d)\s*of\s*3", t, re.I | re.M); rec["review_header"] = hdr
            sev = collections.Counter(re.findall(r"\b(CRITICAL|MAJOR|MINOR)\b", t)); rec["labels"] = dict(sev)
            rec["blocking_ids"] = ids_from(outp)
            rec["blocking_word_count"] = len(re.findall(r"blocking", t, re.I))
    if step != "AUD": rec["spec_after"] = spec_stats(run)
    else: rec["spec_audited"] = spec_stats(run_dir(run)/"aud"/"ws", None) if False else {"bytes": (base/SPEC).stat().st_size}
    st["log"][step] = rec
    if step not in st["done"]: st["done"].append(step)
    save(run, st); print(json.dumps({run: {step: rec}}, indent=1))

def status():
    for run in sorted(p.name for p in RUNS.iterdir()):
        st = load(run); row = []
        for s in STEPS:
            r = st["log"].get(s)
            if r is None: row.append(f"{s}:-")
            else:
                v = r.get("verdict", "ok" if r["output_exists"] else "MISSING")
                row.append(f"{s}:{v}")
        print(run, " ".join(row), "| spec", st["log"].get("V2", st["log"].get("V1", st["log"].get("R1", {}))).get("spec_after", {}).get("bytes"))

def peek(run, step):
    a = arm_of(run); p = ws(run)/OUT[a][step]; t = p.read_text(errors="ignore")
    print("lines with numbered/ids:", len(re.findall(r"(?m)^\s*\|?\s*\**(?:[A-Z]{0,2}-?\d+)[\.\):\| ]", t)))
    for m in re.finditer(r"(?m)^(#{1,4} .*|.*(?:findings?|citation).*count.*)$", t): print(m.group(0)[:140])

if __name__ == "__main__":
    c = sys.argv[1]
    if c == "build":
        build(tuple(int(x) for x in sys.argv[2].split(",")) if len(sys.argv) > 2 else (1,2,3), tuple(int(x) for x in sys.argv[3].split(",")) if len(sys.argv) > 3 else (1,2,3))
    elif c == "prep": prep(sys.argv[2], sys.argv[3], dict(kv.split("=", 1) for kv in sys.argv[4:]))
    elif c == "ingest": ingest(sys.argv[2], sys.argv[3])
    elif c == "status": status()
    elif c == "peek": peek(sys.argv[2], sys.argv[3])
