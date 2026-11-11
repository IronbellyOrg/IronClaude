#!/usr/bin/env python3
"""PN2 harness (design l2): the Stage 2 arm-3 loop with the lint output given to the reviewers. Usage:
  harness.py build [STRATUM]           create sandboxes (sonnet: l2-r1..r6; haiku: l2h-r1..r4) and prepare R1
  harness.py extend                    D4: add l2-r7..r9 once, only when analyze says INCONCLUSIVE from the band
  harness.py prep RUN STEP [K=V ...]   write RUN/PROMPT-STEP.md (STEP in R1 V1 R2 V2 R3 AUD AUD2)
  harness.py ingest RUN STEP           record outputs of a finished step
  harness.py status | basetokens | analyze
Everything except the lint step and the lint sentence of the review briefs is the Stage 2 arm-3 design byte for byte.
Decision constants live in decision.toml. No check in this file or in advance.py reads a token count to stop, skip or
truncate a run (owner decision D6); tokens are summed only after steps have finished."""
import json, os, re, sys, shutil, hashlib, subprocess, pathlib, collections, glob, tomllib
S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S/"scratchpad"; P11 = SP/"p11"; P13 = SP/"p13"; AB = pathlib.Path(os.environ.get("PN2_AB") or P13/"ab2"); RUNS = AB/"runs"; TASKS = S/"tasks"
TASKS_GLOB = os.environ.get("PN2_TASKS_GLOB") or "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"   # worker transcripts (JSONL), C0
S1 = SP/"exp346/.dev/experiments/346-validation/phase2/S1"
REPO = str(P13/"clones/pn2")
BASE_REF = "69ac8b3335564fb5551980e984c5d9b763039cc1"
SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
AUD_CMD_SHA = "e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494"
AUD_RULES_SHA = "3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8"
CFG = tomllib.load(open(AB/"decision.toml", "rb"))
PRODUCT_REF = os.environ.get("PN2_PRODUCT_REF") or CFG["lint"]["product_ref"]
LINT_CHECKS = CFG["lint"]["checks"]
DESIGN = "l2"
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
STEPS = ["R1", "V1", "R2", "V2", "R3", "AUD", "AUD2"]
LOOP_STEPS = ["R1", "V1", "R2", "V2", "R3"]
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
def arm_of(run): return 3            # every l2 run is the arm-3 design
def stratum_of(run): return "haiku" if run.startswith("l2h-") else "sonnet"
def model_for(run, step):
    """Loop workers follow the stratum; the frozen audits are always sonnet (D3)."""
    if step in ("AUD", "AUD2"): return "sonnet"
    return CFG["strata"]["haiku_model"] if stratum_of(run) == "haiku" else "sonnet"
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

def build(stratum="sonnet", reps=None):
    """Create the sandboxes of one stratum. command.md and the rules file come from PRODUCT_REF."""
    assert PRODUCT_REF and not PRODUCT_REF.startswith("PRODUCT_REF"), "set lint.product_ref in decision.toml"
    cmd = git_show(PRODUCT_REF, "src/superclaude/commands/spec-panel.md")
    assert hashlib.sha256(cmd.encode()).hexdigest() == AUD_CMD_SHA, "spec-panel command differs from the frozen audit command"
    rules = git_show(PRODUCT_REF, "src/superclaude/rules/prompts/document_review_loop_prompts.md")
    prefix = "l2h" if stratum == "haiku" else "l2"
    reps = reps or tuple(range(1, (CFG["strata"]["haiku_n"] if stratum == "haiku" else CFG["strata"]["sonnet_n"]) + 1))
    assert sha(S1/"inputs/repo-overlay"/SPEC) == SPEC_SHA
    assert sha(P11/"rules.md") == AUD_RULES_SHA
    for r in reps:
        run = f"{prefix}-r{r}"; d = run_dir(run)
        if d.exists(): print('skip existing', run); continue
        (d/"home/.claude/rules/prompts").mkdir(parents=True)
        shutil.copytree(S1/"inputs/repo-overlay", d/"ws")
        (d/"ws"/D/"review").mkdir(parents=True); (d/"ws"/D/"specs/history").mkdir(parents=True)
        (d/"command.md").write_text(cmd)
        (d/"home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules)
        save(run, {"run": run, "arm": 3, "design": DESIGN, "stratum": stratum, "rep": r, "done": [], "log": {}})
        prep(run, "R1", {})
    print("built", sorted(p.name for p in RUNS.iterdir()))

def extend():
    """D4: one adaptive extension of the Sonnet stratum by 3 replicates, never a second time."""
    flag = AB/"extension.json"
    if flag.exists(): raise SystemExit("extension already used; a second extension needs the owner")
    n0 = CFG["strata"]["sonnet_n"]; k = CFG["strata"]["sonnet_extra"]
    build("sonnet", tuple(range(n0 + 1, n0 + k + 1)))
    flag.write_text(json.dumps({"extended_to": n0 + k, "runs": [f"l2-r{i}" for i in range(n0 + 1, n0 + k + 1)]}))

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
    body = sec.group(1)
    # fix 2026-11-10 (l2-r6 mis-parse 'F1, WC-4'): ids named in "... blocking finding ids ...: <ids>" or a "Blocking findings:" list win over ids mentioned in prose
    m2 = re.search(r"(?i)blocking (?:finding )?ids?[^:\n]{0,40}:\s*([^\n]+)", body)
    if m2:
        found = re.findall(r"\b(?:R\d-)?[A-Z]{1,2}-?\d+\b", m2.group(1))
        found = [x for i, x in enumerate(found) if x not in found[:i] and not x.startswith(("FR", "AC", "SHA"))]
        if found: return ", ".join(found)
    bl = re.search(r"(?ims)^\W*Blocking findings\W*:\s*\n(.*)\Z", body)
    if bl:
        found = []
        for x in re.findall(r"(?m)^\s*[-*]\s*\**((?:R\d-)?[A-Z]{1,2}-?\d+)\b", bl.group(1)):
            if x not in found: found.append(x)
        if found: return ", ".join(found)
    para = "\n".join([l for l in body.splitlines() if l.strip()][:3])
    toks = []
    for x in re.findall(r"\b(?:R\d-)?[A-Z]{1,2}-?\d+\b", para):
        if x not in toks and not x.startswith(("FR", "AC", "SHA")): toks.append(x)
    return ", ".join(toks) or None

def lint_rel(n): return f"{D}/review/lint-{n}.md"

def run_lint(run, n):
    """Deterministic lint step (no model): lint-<n>.md for the candidate as it is now. Recorded in state['log']['LINT<n>']."""
    out = ws(run)/lint_rel(n)
    r = subprocess.run(["uv", "run", "--project", REPO, "superclaude", "review", "lint", str(ws(run)/SPEC), "--format", "md",
                        "--checks", LINT_CHECKS, "--out", str(out)], capture_output=True, text=True)
    assert r.returncode == 0 and out.exists(), f"lint failed for {run}: {r.stderr}"
    text = out.read_text()
    st = load(run); st["log"][f"LINT{n}"] = {"checks": LINT_CHECKS, "findings": len(re.findall(r"(?m)^### LINT-", text)),
                                            "sha256": hashlib.sha256(text.encode()).hexdigest(), "spec_sha256": sha(ws(run)/SPEC)}
    save(run, st)

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
        if a == 3: body = (f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={spec}, lint={lint_rel(1)}.")
        else: body = "Follow this review prompt:\n" + prompt_text("FIRST-REVIEW prompt", {"CANDIDATE": spec})
        return f"{head} {body}\nWrite the full report to {out}. Do not edit anything else. {ctx}"
    if step in ("R2", "R3"):
        n = 2 if step == "R2" else 3
        prior = OUT[a]["R1" if n == 2 else "R2"]; base = f"{H}/spec-v{n-1}.md"
        head = f"Run /sc:spec-panel @{spec} {FLAGS} --re-review {prior} --baseline {base} ."
        vals = {"CANDIDATE": spec, "BASELINE": base, "PRIOR": prior, "N": str(n)}
        if a == 3: body = (f"Re-review per the RE-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. "
                           f"Values: candidate={spec}, baseline={base}, prior={prior}, lint={lint_rel(n)}.")
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
    if step in ("R1", "R2", "R3"): run_lint(run, {"R1": 1, "R2": 2, "R3": 3}[step])
    if step in ("AUD", "AUD2"):
        ad = d/("aud" if step == "AUD" else "aud2")
        if ad.exists(): shutil.rmtree(ad)
        (ad/"home/.claude/rules/prompts").mkdir(parents=True)
        shutil.copytree(S1/"inputs/repo-overlay", ad/"ws")
        (ad/"ws"/D/"review").mkdir(parents=True)
        shutil.copy(ws(run)/SPEC, ad/"ws"/SPEC)
        git_cmd = git_show(BASE_REF, "src/superclaude/commands/spec-panel.md")
        assert hashlib.sha256(git_cmd.encode()).hexdigest() == AUD_CMD_SHA and sha(P11/"rules.md") == AUD_RULES_SHA, "audit instrument is not the frozen one"
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
    base = (run_dir(run)/("aud" if step == "AUD" else "aud2")/"ws") if step in ("AUD", "AUD2") else ws(run)
    outp = base/(AUD_OUT if step in ("AUD", "AUD2") else OUT[a][step])
    rec = {"output_exists": outp.exists()}
    if outp.exists():
        t = outp.read_text(errors="ignore"); rec["report_bytes"] = len(t.encode())
        if step in ("R1", "R2", "R3", "AUD", "AUD2"):
            vs = re.findall(r"verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)", t, re.I); rec["verdict"] = vs[-1].upper() if vs else "NONE"
            hdr = re.findall(r"^\W*review:\s*(\d)\s*of\s*3", t, re.I | re.M); rec["review_header"] = hdr
            sev = collections.Counter(re.findall(r"\b(CRITICAL|MAJOR|MINOR)\b", t)); rec["labels"] = dict(sev)
            rec["blocking_ids"] = ids_from(outp)
            rec["blocking_word_count"] = len(re.findall(r"blocking", t, re.I))
    if step not in ("AUD", "AUD2"): rec["spec_after"] = spec_stats(run)
    else: rec["spec_audited"] = {"bytes": (base/SPEC).stat().st_size}
    rec["stratum"] = st.get("stratum", stratum_of(run)); rec["model"] = model_for(run, step)
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
                v = "LOST" if r.get("lost") else r.get("verdict", "ok" if r.get("output_exists") else "MISSING")
                row.append(f"{s}:{v}")
        lint = "/".join(str(st["log"].get(f"LINT{i}", {}).get("findings", "-")) for i in (1, 2, 3))
        print(run, st.get("stratum", stratum_of(run)), " ".join(row), "| lint", lint, "| spec", st["log"].get("V2", st["log"].get("V1", st["log"].get("R1", {}))).get("spec_after", {}).get("bytes"))

def basetokens():
    """Recompute the Stage 2 arm-3 baseline (C9.1, D2) from the p11 transcripts: per-run loop A, one audit, B."""
    import analysis
    base = analysis.baseline_tokens(TASKS_GLOB)
    if not base: print("no p11 transcripts found; cannot recompute"); return None
    loops = [v["loop"] for v in base.values()]; auds = [v["aud"] for v in base.values() if v["aud"]]
    for run, v in base.items(): print(run, "loop", v["loop"], "aud", v["aud"], "steps", v["steps"])
    a = sum(loops)/len(loops); u = sum(auds)/len(auds) if auds else None
    print(f"A_BASE (loop only) = {a:.0f}; one audit = {u and round(u)}; B_BASE = {u and round(a+u)}  (stated: 100424 / 69044 / 169468)")
    r1 = [v["steps"].get("R1") for v in base.values() if v["steps"].get("R1")]
    print("R1 mean", round(sum(r1)/len(r1)) if r1 else None)
    return base

def analyze():
    import analysis
    r = analysis.analyze()
    print(r["decision"], "|", "; ".join(r["reasons"])); 
    if r["next_action"]: print(r["next_action"])

def peek(run, step):
    a = arm_of(run); p = ws(run)/OUT[a][step]; t = p.read_text(errors="ignore")
    print("lines with numbered/ids:", len(re.findall(r"(?m)^\s*\|?\s*\**(?:[A-Z]{0,2}-?\d+)[\.\):\| ]", t)))
    for m in re.finditer(r"(?m)^(#{1,4} .*|.*(?:findings?|citation).*count.*)$", t): print(m.group(0)[:140])

if __name__ == "__main__":
    c = sys.argv[1]
    if c == "build": build(sys.argv[2] if len(sys.argv) > 2 else "sonnet")
    elif c == "extend": extend()
    elif c == "prep": prep(sys.argv[2], sys.argv[3], dict(kv.split("=", 1) for kv in sys.argv[4:]))
    elif c == "ingest": ingest(sys.argv[2], sys.argv[3])
    elif c == "status": status()
    elif c == "basetokens": basetokens()
    elif c == "analyze": analyze()
    elif c == "peek": peek(sys.argv[2], sys.argv[3])
