#!/usr/bin/env python3
"""Baseline drift check: exact replay of Stage 2 arm 3 (p11 a3) run now, 2 replicates a3d-r1 / a3d-r2.
Loop: Sonnet workers, steps R1 V1 R2 V2 R3 (R1 FAIL -> V1 -> R2; PASS ends the loop; after R3 always audit),
then two frozen Sonnet audits AUD and AUD2 (fresh sandboxes aud/ and aud2/, same brief/command/rules as p11 AUD).
Copy-and-modify of $SP/p11/harness.py restricted to arm 3.  p11 is only READ.

  harness.py build | prep RUN STEP [IDS=..] | ingest RUN STEP | status | unlaunch RUN STEP | tokens | analyze
Run with python3 (stdlib only)."""
import collections
import datetime
import glob
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys

S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S / "scratchpad"
P11 = SP / "p11"
HERE = pathlib.Path(__file__).resolve().parent
RUNS = HERE / "runs"
S1 = SP / "exp346/.dev/experiments/346-validation/phase2/S1"
CENTRAL = SP / "central"
TASKS_GLOB = "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"
MAX_CONCURRENT = 6
RUN_NAMES = ["a3d-r1", "a3d-r2", "a3d-r3", "a3d-r4", "a3d-r5", "a3d-r6"]
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
HIST = f"{D}/specs/history"
SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
CMD_SHA = "e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494"     # p11 a3 command == frozen audit command
RULES_SHA = "3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8"   # p11 rules file
STEPS = ["R1", "V1", "R2", "V2", "R3", "AUD", "AUD2"]
LOOP_STEPS = ["R1", "V1", "R2", "V2", "R3"]
AUDS = ("AUD", "AUD2")
FLAGS = "--mode critique --focus requirements,architecture"
OUT = {"R1": f"{D}/review/round1.md", "V1": f"{D}/review/revise1.md", "R2": f"{D}/review/round2.md",
       "V2": f"{D}/review/revise2.md", "R3": f"{D}/review/round3.md"}
AUD_OUT = f"{D}/review/audit.md"
P11_A, P11_AUD_MEAN, P11_LOOP_MEAN = None, 69044, 100424     # expected basetokens values (drift sanity)

sys.path.insert(0, str(CENTRAL))
import score_themes as sc  # noqa: E402


def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
def run_dir(run): return RUNS / run
def load(run): return json.load(open(run_dir(run) / "state.json"))
def save(run, st): json.dump(st, open(run_dir(run) / "state.json", "w"), indent=1)
def ws(run): return run_dir(run) / "ws"
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def sha_text(t): return hashlib.sha256(t.encode()).hexdigest()
def all_runs(): return sorted(p.name for p in RUNS.iterdir() if (p / "state.json").exists()) if RUNS.exists() else []
def norm(s): return " ".join(s.split())


def spec_stats(base):
    b = (pathlib.Path(base) / SPEC).read_bytes()
    return {"bytes": len(b), "lines": b.count(b"\n"), "sha256": hashlib.sha256(b).hexdigest()}


def section(text, title):
    m = re.search(rf"^### {re.escape(title)}\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    return m.group(1).strip()


def inputs():
    cmd = (P11 / "runs/a3-r1/command.md").read_text()
    rules = (P11 / "rules.md").read_text()
    assert sha_text(cmd) == CMD_SHA, "p11 a3 command hash changed"
    assert sha_text(rules) == RULES_SHA, "p11 rules hash changed"
    return cmd, rules


def sandbox(d, cmd, rules):
    """Same layout as p11 build (arm 3): overlay copy, review/, specs/history/, rules file under home, command.md."""
    d = pathlib.Path(d)
    (d / "home/.claude/rules/prompts").mkdir(parents=True)
    shutil.copytree(S1 / "inputs/repo-overlay", d / "ws")
    (d / "ws" / D / "review").mkdir(parents=True)
    (d / "ws" / D / "specs/history").mkdir(parents=True)
    (d / "command.md").write_text(cmd)
    (d / "home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules)
    assert sha(d / "ws" / SPEC) == SPEC_SHA, "spec hash mismatch"


def build():
    cmd, rules = inputs()
    for run in RUN_NAMES:
        d = run_dir(run)
        if d.exists():
            print("skip existing", run)
            continue
        RUNS.mkdir(exist_ok=True)
        sandbox(d, cmd, rules)
        save(run, {"run": run, "arm": 3, "rep": int(run.split("-r")[1]), "loop_model": "sonnet", "done": [], "prepared": [],
                   "transitioned": [], "log": {}, "launched": {}, "relaunch": {}, "loop_end": None, "lost": False, "complete": False})
    print("built", all_runs())


# ---------------------------------------------------------------- briefs (verbatim copy of p11 new_brief, arm 3 only)
def ids_from(report_path):
    """p11's parser (used for the baseline's V briefs)."""
    t = pathlib.Path(report_path).read_text(errors="ignore")
    m = re.findall(r"(?im)^\W*(?:\*\*)?(?:Reviser brief\W*)?Blocking (?:finding )?ids?\W*[:\-]\s*(.+)$", t)
    if m:
        return m[-1].strip(" *.")
    sec = re.search(r"(?ms)^#+\s*Reviser brief[^\n]*\n(.*?)(?=^#+ |^verdict:|\Z)", t)
    if not sec:
        return None
    para = "\n".join([ln for ln in sec.group(1).splitlines() if ln.strip()][:3])
    toks = []
    for x in re.findall(r"\b(?:R\d-)?[A-Z]{1,2}-?\d+\b", para):
        if x not in toks and not x.startswith(("FR", "AC", "SHA")):
            toks.append(x)
    return ", ".join(toks) or None


def new_brief(step, ids):
    spec = SPEC
    H = HIST
    ctx = (f"First read {D}/README.md (binding shared context; the files under {D}/inventory/ are the only evidence you can check, "
           f"mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file(s).")
    if step == "R1":
        head = f"Run /sc:spec-panel @{spec} {FLAGS} ."
        body = f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={spec}."
        return f"{head} {body}\nWrite the full report to {OUT['R1']}. Do not edit anything else. {ctx}"
    if step in ("R2", "R3"):
        n = 2 if step == "R2" else 3
        prior = OUT["R1" if n == 2 else "R2"]
        base = f"{H}/spec-v{n-1}.md"
        head = f"Run /sc:spec-panel @{spec} {FLAGS} --re-review {prior} --baseline {base} ."
        body = (f"Re-review per the RE-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. "
                f"Values: candidate={spec}, baseline={base}, prior={prior}.")
        return f"{head} {body}\nWrite the full report to {OUT[step]}. Do not edit anything else. {ctx}"
    if step in ("V1", "V2"):
        n = 1 if step == "V1" else 2
        rep = OUT["R1" if n == 1 else "R2"]
        idv = ids or "the blocking findings listed in the report"
        body = (f"Revise per the REVISE prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. "
                f"Values: candidate={spec}, IDS={idv}.")
        return (f"{body}\nInputs: the review report {rep} (its Reviser brief lists the blocking ids), the spec, and the files under {D}/inventory/. "
                f"Edit the spec {spec} in place; it is the only file you may change besides your output. Do not run the spec-panel. "
                f"Write {OUT[step]} with the byte accounting the prompt asks for and one row per finding id (applied where, or rejected with a cited reason). {ctx}")
    raise ValueError(step)


def audit_brief():
    return (f"Run /sc:spec-panel @{SPEC} {FLAGS} . This is a labelled whole-document audit of the final spec: a first review of the whole document. "
            f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={SPEC}.\n"
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


def wrap(sb, brief, with_cmd):
    return WRAP.format(sb=sb, wsdir="ws", cmdpart=CMDPART.format(sb=sb) if with_cmd else "", brief=brief)


def mark_prepared(run, step):
    st = load(run)
    if step not in st["prepared"]:
        st["prepared"].append(step)
    save(run, st)


def prep(run, step, subs=None):
    subs = subs or {}
    d = run_dir(run)
    if step in AUDS:
        ad = d / ("aud" if step == "AUD" else "aud2")
        if ad.exists():
            shutil.rmtree(ad)
        cmd, rules = inputs()
        sandbox(ad, cmd, rules)
        shutil.copy(ws(run) / SPEC, ad / "ws" / SPEC)
        text = wrap(ad, audit_brief(), True)
    else:
        if step in ("V1", "V2"):
            shutil.copy(ws(run) / SPEC, ws(run) / HIST / f"spec-v{step[1]}.md")
            ids = subs.get("IDS") or ids_from(ws(run) / OUT["R1" if step == "V1" else "R2"])
            print("IDS =", ids)
        else:
            ids = None
        text = wrap(d, new_brief(step, ids), step in ("R1", "R2", "R3"))
    p = d / f"PROMPT-{step}.md"
    p.write_text(text)
    mark_prepared(run, step)
    print(p)
    return p


def out_path(run, step):
    d = run_dir(run)
    if step == "AUD":
        return d / "aud/ws" / AUD_OUT
    if step == "AUD2":
        return d / "aud2/ws" / AUD_OUT
    return ws(run) / OUT[step]


def ingest(run, step):
    st = load(run)
    outp = out_path(run, step)
    rec = {"output_exists": outp.exists()}
    old = st["log"].get(step, {})
    if "output_tokens" in old:
        rec["output_tokens"] = old["output_tokens"]
    if outp.exists():
        t = outp.read_text(errors="ignore")
        rec["report_bytes"] = len(t.encode())
        if step in ("R1", "R2", "R3") + AUDS:
            rec["verdict"] = sc.verdict_of(t)
            rec["review_header"] = re.findall(r"^\W*review:\s*(\d)\s*of\s*3", t, re.I | re.M)
            rec["labels"] = dict(collections.Counter(re.findall(r"\b(CRITICAL|MAJOR|MINOR)\b", t)))
            rec["blocking_ids"] = ids_from(outp)
            rec["blocking_word_count"] = len(re.findall(r"blocking", t, re.I))
    if step in AUDS:
        base = run_dir(run) / ("aud" if step == "AUD" else "aud2") / "ws"
        rec["spec_audited"] = {"bytes": (base / SPEC).stat().st_size}
    else:
        rec["spec_after"] = spec_stats(ws(run))
    st["log"][step] = rec
    if step not in st["done"]:
        st["done"].append(step)
    save(run, st)
    print(json.dumps({run: {step: {k: v for k, v in rec.items() if k != "labels"}}}, indent=1))
    return rec


def unlaunch(run, step, quiet=False):
    """Drop a ledger entry so the step is relaunched. The second call for the same step marks the run lost."""
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


# ---------------------------------------------------------------- transcripts / tokens (matched by prompt TEXT)
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
    """tokens = sum over distinct assistant message ids of max output_tokens (a message is logged once per content block)."""
    try:
        lines = pathlib.Path(path).read_text(errors="ignore").splitlines()
    except Exception:
        return None
    first = first_user_text(lines)
    ids, models, done, last_text, anon = {}, collections.Counter(), False, "", 0
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


def prompt_index():
    """norm(prompt text) -> (run, step) for every existing PROMPT file of these runs."""
    idx = {}
    for run in all_runs():
        for p in run_dir(run).glob("PROMPT-*.md"):
            if ".failed" in p.name:
                continue
            idx[norm(p.read_text())] = (run, p.stem.replace("PROMPT-", ""))
    return idx


def scan_transcripts(tasks_glob=None, pidx=None):
    """-> {(run, step): [info]} for transcripts whose first user message IS a PROMPT text (whitespace-normalised);
    falls back to 'PROMPT text contained in the first message' (a wrapper around the pasted prompt)."""
    pidx = prompt_index() if pidx is None else pidx
    out = collections.defaultdict(list)
    for f in sorted(glob.glob(tasks_glob or TASKS_GLOB)):
        info = transcript_info(f)
        if not info or not info["first"]:
            continue
        key = norm(info["first"])
        k = pidx.get(key)
        if k is None and "scratchpad/p16/base-drift/runs/" in key:
            for t, kk in pidx.items():
                if t in key:
                    k = kk
                    break
        if k:
            out[k].append(info)
    return out


def pick(cands, expected, label=""):
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


def tokens_cmd():
    idx = scan_transcripts()
    for run in all_runs():
        st = load(run)
        for step in STEPS:
            c = idx.get((run, step))
            if not c:
                continue
            best = pick(c, "sonnet", f"{run} {step}")
            if best and step in st["log"]:
                st["log"][step]["output_tokens"] = best["tokens"]
        save(run, st)
        print(run, "loop", sum(st["log"].get(s, {}).get("output_tokens", 0) for s in LOOP_STEPS),
              "aud", st["log"].get("AUD", {}).get("output_tokens"), "aud2", st["log"].get("AUD2", {}).get("output_tokens"))


# ---------------------------------------------------------------- status / analyze
def status():
    for run in all_runs():
        st = load(run)
        row = []
        for s in STEPS:
            r = st["log"].get(s)
            row.append(f"{s}:-" if r is None else f"{s}:{r.get('verdict', 'ok' if r['output_exists'] else 'MISSING')}")
        print(run, " ".join(row), "| loop_end", st["loop_end"], "LOST" if st["lost"] else ("complete" if st["complete"] else ""))


def p11_step_means():
    """Per-step mean output tokens of the p11 baseline, read from `$SP/p12/ab1/harness.py basetokens` (prompt-text-independent
    legacy path matching).  -> ({step: mean over runs having it}, loop_mean, audit_mean) or None when it cannot be run."""
    import ast
    try:
        out = subprocess.run([sys.executable, "harness.py", "basetokens"], cwd=SP / "p12/ab1", capture_output=True, text=True, timeout=300).stdout
    except Exception:
        return None
    per = collections.defaultdict(list)
    for m in re.finditer(r"^a3-r\d loop \d+ audit \d+ (\{.*\})$", out, re.M):
        for k, v in ast.literal_eval(m.group(1)).items():
            per[k].append(v)
    if len(per.get("R1", [])) != 6:
        return None
    ml = re.search(r"loop mean ([\d,]+)", out)
    ma = re.search(r"audit mean ([\d,]+)", out)
    means = {k: sum(v) / len(v) for k, v in per.items()}
    return means, int(ml.group(1).replace(",", "")), int(ma.group(1).replace(",", ""))


def blocking_of(path):
    """Same scorer as the central matrix (build_matrix._audit_blk): None unless the verdict is PASS/FAIL."""
    p = pathlib.Path(path)
    if not p.exists():
        return None, "MISSING"
    v = sc.verdict_of(p.read_text(errors="ignore"))
    if v not in ("PASS", "FAIL"):
        return None, v
    return len(sc.blocking_findings(p)), v


def fmt(x):
    return "-" if x is None else f"{x:,.0f}"


def analyze():
    base = p11_step_means()
    if base:
        means, p11_loop, p11_aud = base
        if p11_loop != P11_LOOP_MEAN or p11_aud != P11_AUD_MEAN:
            print(f"WARN p11 basetokens means {p11_loop}/{p11_aud} differ from expected {P11_LOOP_MEAN}/{P11_AUD_MEAN}")
    else:
        print("WARN could not run basetokens; using recorded p11 loop/audit means only")
        means, p11_loop, p11_aud = {}, P11_LOOP_MEAN, P11_AUD_MEAN
    print("p11 per-step mean output tokens: " + ", ".join(f"{k} {v:,.0f}" for k, v in sorted(means.items())) +
          f" | loop mean {p11_loop:,} audit mean {p11_aud:,}")
    print("\nrun       loop A     R1       audit1   audit2   blk1  blk2  verdicts      loop_end  reviews")
    loops, r1s, auds, blks, steps_acc = [], [], [], [], collections.defaultdict(list)
    for run in all_runs():
        st = load(run)
        log = st["log"]
        miss = [s for s in LOOP_STEPS if s in log and "output_tokens" not in log[s]]
        loop = sum(log.get(s, {}).get("output_tokens", 0) for s in LOOP_STEPS)
        r1 = log.get("R1", {}).get("output_tokens")
        a1, a2 = log.get("AUD", {}).get("output_tokens"), log.get("AUD2", {}).get("output_tokens")
        b1, v1 = blocking_of(out_path(run, "AUD"))
        b2, v2 = blocking_of(out_path(run, "AUD2"))
        reviews = sum(1 for s in ("R1", "R2", "R3") if s in log)
        print(f"{run:8} {fmt(loop):>8} {fmt(r1):>8} {fmt(a1):>8} {fmt(a2):>8} {str(b1):>5} {str(b2):>5}  {v1}/{v2:<8} {str(st['loop_end']):9} {reviews}"
              + (f"  tokens_missing={miss}" if miss else "") + ("  LOST" if st["lost"] else ""))
        if st["complete"] and not miss and loop:
            loops.append(loop)
            r1s.append(r1)
            for s in LOOP_STEPS:
                if s in log:
                    steps_acc[s].append(log[s]["output_tokens"])
            auds += [x for x in (a1, a2) if x]
            blks += [b for b in (b1, b2) if b is not None]
    if not loops:
        print("\nno completed runs yet")
        return
    ml, mr1, ma = sum(loops) / len(loops), sum(r1s) / len(r1s), (sum(auds) / len(auds) if auds else None)
    print(f"\ncompleted runs n={len(loops)}: fresh loop mean {ml:,.0f} (p11 {p11_loop:,}) ratio {ml / p11_loop:.2f}")
    if "R1" in means:
        print(f"fresh R1 mean {mr1:,.0f} (p11 {means['R1']:,.0f}) ratio {mr1 / means['R1']:.2f}")
    for s in LOOP_STEPS[1:]:
        if steps_acc.get(s) and s in means:
            m = sum(steps_acc[s]) / len(steps_acc[s])
            print(f"fresh {s} mean {m:,.0f} over {len(steps_acc[s])} runs (p11 {means[s]:,.0f} over runs having it) ratio {m / means[s]:.2f}")
    if ma:
        print(f"fresh audit mean {ma:,.0f} (p11 {p11_aud:,}) ratio {ma / p11_aud:.2f}")
    if blks:
        print(f"fresh blocking per audit mean {sum(blks) / len(blks):.2f} over {len(blks)} scored audits (baseline matrix BLK 1.50)")
    print("note: 'drift' is judged on loop and R1 ratios; p11 values are from the same prompt-independent basetokens method.")


def main(argv):
    c = argv[1]
    if c == "build":
        build()
    elif c == "prep":
        prep(argv[2], argv[3], dict(kv.split("=", 1) for kv in argv[4:]))
    elif c == "ingest":
        ingest(argv[2], argv[3])
    elif c == "status":
        status()
    elif c == "unlaunch":
        unlaunch(argv[2], argv[3])
    elif c == "tokens":
        tokens_cmd()
    elif c == "analyze":
        analyze()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
