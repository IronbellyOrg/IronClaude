#!/usr/bin/env python3
"""PN1 harness (design b1): independent reviewer panel + deterministic merge + typed finding ledger.

Derived from the Stage 2 harness ($SP/p11/harness.py). Byte-for-byte from p11: S1, D, SPEC, FLAGS, AUD_OUT, WRAP, CMDPART,
section(), git_show(), the arm-3 brief texts (generalised only by passing out/prior/base/rep as arguments) and the AUD brief.

Usage:
  harness.py build [--stratum sonnet|haiku]   create the sandboxes (sonnet: o2-r1..r6; haiku: o2h-r1..r4)
  harness.py extend                           D4: once, only when the Sonnet n=6 result is INCONCLUSIVE, add o2-r7..r9
  harness.py status                           table of all runs
  harness.py unlaunch RUN STEP                forget a launch so the step can be launched again
  harness.py basetokens                       recompute A_BASE / one audit / B_BASE from the p11 transcripts (C9.1)
  harness.py outcomes                         write outcome telemetry (catalog-v1 or theme-v1, and adjudicated-v1)
  harness.py analyze                          write RESULTS.md
Steps: R<n>.<reviewer id>, M<n>, ADJ, V<n>, L<n>, AUD, AUD2.  Cost never stops a run (D6): token counts are read only after a step finished.
"""
import collections, hashlib, importlib.util, json, os, pathlib, random, re, shutil, subprocess, sys, time
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import analysis as A  # noqa: E402
import c93  # noqa: E402

S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S / "scratchpad"
P11 = SP / "p11"
P13 = SP / "p13"
AB = SP / "p19/rep/pn1o"
RUNS = AB / "runs"
REPO = str(SP / "p19/clones/pn1o")
S1 = SP / "exp346/.dev/experiments/346-validation/phase2/S1"
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
FLAGS = "--mode critique --focus requirements,architecture"
AUD_OUT = f"{D}/review/audit.md"
RULES_REL = "src/superclaude/rules/prompts/document_review_loop_prompts.md"
CMD_REL = "src/superclaude/commands/spec-panel.md"
BASE_REF = "69ac8b3335564fb5551980e984c5d9b763039cc1"
SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
AUD_CMD_SHA = "e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494"
AUD_RULES_SHA = "3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8"
PRODUCT_REF = "5798a7b950ef1203c514a887f999997045de5582"
TASKS_GLOB = "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"
MAX_CONCURRENT = 9
# LIVE ADAPTATION (kit): panel resolution inputs come from the environment so one harness serves every Stage C panel.
#   PN_ENV   environment name in the tier file (default anthropic-only; use gateway live)
#   PN_PANEL panel template: a file path or @NAME (packaged), e.g. an eval panel written by render.py
#   PN_TIERS tier file (an eval tiers file with the tier2b models filled in)
PANEL_ARGS = ["--env", os.environ.get("PN_ENV", "anthropic-only")]
if os.environ.get("PN_PANEL"):
    PANEL_ARGS += ["--template", os.environ["PN_PANEL"]]
if os.environ.get("PN_TIERS"):
    PANEL_ARGS += ["--tiers", os.environ["PN_TIERS"]]
DESIGN = "o2"
CLI = ["uv", "run", "--project", REPO, "superclaude", "review"]
TELEMETRY_DIR = SP / "p19/clones/pn1o/.dev/benchmarks/review-telemetry"
CATALOG = P13 / "catalog/catalog.json"
SETTLE_S = 180          # no transcript: output unchanged this long means finished
STALE_S = 3600          # no output after this long: WARN stale (a warning only; D6: never a kill)
RETRIES = 1


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rules():
    return A.load_rules()


# ---------------------------------------------------------------- byte-for-byte p11 pieces
def git_show(ref, path):
    return subprocess.run(["git", "-C", REPO, "show", f"{ref}:{path}"], check=True, capture_output=True, text=True).stdout


def section(text, title):
    m = re.search(rf"^### {re.escape(title)}\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    return m.group(1).strip()


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
CTX = (f"First read {D}/README.md (binding shared context; the files under {D}/inventory/ are the only evidence you can check, "
       f"mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file(s).")
RULES_PTR = "~/.claude/rules/prompts/document_review_loop_prompts.md"


def brief(step, *, out, prior=None, base=None, rep=None, ids=None):
    """The arm-3 briefs of p11 (strings unchanged); out/prior/base/rep are passed in."""
    spec = SPEC
    if step == "R1":
        head = f"Run /sc:spec-panel @{spec} {FLAGS} ."
        body = f"Review per the FIRST-REVIEW prompt in {RULES_PTR}. Values: candidate={spec}."
        return f"{head} {body}\nWrite the full report to {out}. Do not edit anything else. {CTX}"
    if step in ("R2", "R3"):
        head = f"Run /sc:spec-panel @{spec} {FLAGS} --re-review {prior} --baseline {base} ."
        body = (f"Re-review per the RE-REVIEW prompt in {RULES_PTR}. "
                f"Values: candidate={spec}, baseline={base}, prior={prior}.")
        return f"{head} {body}\nWrite the full report to {out}. Do not edit anything else. {CTX}"
    if step in ("V1", "V2"):
        vals = {"CANDIDATE": spec, "IDS": ids or "the blocking findings listed in the report"}
        body = (f"Revise per the REVISE prompt in {RULES_PTR}. "
                f"Values: candidate={spec}, IDS={vals['IDS']}.")
        return (f"{body}\nInputs: the review report {rep} (its Reviser brief lists the blocking ids), the spec, and the files under {D}/inventory/. "
                f"Edit the spec {spec} in place; it is the only file you may change besides your output. Do not run the spec-panel. "
                f"Write {out} with the byte accounting the prompt asks for and one row per finding id (applied where, or rejected with a cited reason). {CTX}")
    raise ValueError(step)


def aud_brief():
    return (f"Run /sc:spec-panel @{SPEC} {FLAGS} . This is a labelled whole-document audit of the final spec: a first review of the whole document. "
            f"Review per the FIRST-REVIEW prompt in {RULES_PTR}. Values: candidate={SPEC}.\n"
            f"Write the full report to {AUD_OUT}. Do not edit anything else. First read {D}/README.md (binding shared context; the files under {D}/inventory/ "
            f"are the only evidence you can check, mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file.")


ADJ_BRIEF = ("Read .dev/orca-command-refactor/README.md and the spec .dev/orca-command-refactor/specs/orca-worker-contract-spec.md. "
             "For each finding X<k> in .dev/orca-command-refactor/review/adj-input.md decide whether it is a real defect that blocks implementation: "
             "write the sentence \"An implementer who follows the stated text as written builds X, and X is wrong because Y.\" and confirm it only if "
             "that sentence holds with no further assumption. Write .dev/orca-command-refactor/review/adj.md ending with a fenced block with info string "
             "adj-v1 holding one JSON line per finding: {\"x\": \"X1\", \"verdict\": \"confirmed\" or \"rejected\" or \"unsure\", \"reason\": \"<one sentence>\"}. "
             "Do not edit anything else.")


# ---------------------------------------------------------------- state
def run_dir(run):
    return RUNS / run


def ws(run):
    return run_dir(run) / "ws"


def load(run):
    return json.loads((run_dir(run) / "state.json").read_text())


def save(run, st):
    tmp = run_dir(run) / "state.json.tmp"
    tmp.write_text(json.dumps(st, indent=1))
    tmp.replace(run_dir(run) / "state.json")


def all_runs(strata=None):
    out = []
    if RUNS.exists():
        for p in sorted(RUNS.iterdir()):
            if (p / "state.json").exists():
                if strata is None or stratum_of(p.name) in strata:
                    out.append(p.name)
    return out


def stratum_of(run):
    return "haiku" if run.startswith("o2h-") else "sonnet"


def arm_of(run):
    return 3


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def spec_stats(base):
    p = pathlib.Path(base) / SPEC
    b = p.read_bytes()
    return {"bytes": len(b), "lines": b.count(b"\n"), "sha256": hashlib.sha256(b).hexdigest()}


def cli(*args, ok=(0,)):
    r = subprocess.run([*CLI, *map(str, args)], capture_output=True, text=True)
    if r.returncode not in ok:
        raise RuntimeError(f"review CLI failed ({r.returncode}): {' '.join(map(str, args))}\n{r.stdout}\n{r.stderr}")
    return r


_FM = None


def findings_mod():
    """parse_block comes from the product file itself (standard library only), loaded by path so the harness runs without the package."""
    global _FM
    if _FM is None:
        spec = importlib.util.spec_from_file_location("pn1_findings", pathlib.Path(REPO) / "src/superclaude/cli/review/findings.py")
        _FM = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_FM)
    return _FM


def reviewers_of(st, n):
    pr = st["panel"] if n == 1 else st["panel_rr"]
    return [r["reviewer_id"] for r in pr["reviewers"]]


def reviewer_row(st, n, rid):
    pr = st["panel"] if n == 1 else st["panel_rr"]
    return next(r for r in pr["reviewers"] if r["reviewer_id"] == rid)


# ---------------------------------------------------------------- build
def new_state(run, stratum, rep):
    return {"run": run, "arm": 3, "design": DESIGN, "stratum": stratum, "rep": rep, "round": 1, "phase": "review",
            "launched": {}, "done": [], "lost": [], "retries": {}, "log": {}, "ingested_reviewers": [],
            "telemetry_ids": {}, "created": now()}


def build(stratum="sonnet", reps=None):
    r = rules()
    reps = reps or list(range(1, (r["strata"]["sonnet_runs"] if stratum == "sonnet" else r["strata"]["haiku_runs"]) + 1))
    cmd = git_show(PRODUCT_REF, CMD_REL)
    assert hashlib.sha256(cmd.encode()).hexdigest() == AUD_CMD_SHA, "spec-panel.md changed: it must equal the frozen audit command"
    rules_txt = git_show(PRODUCT_REF, RULES_REL)
    assert "### Findings block" in rules_txt and "### Review panel" in rules_txt, "product rules file lacks the panel text"
    spec_src = S1 / "inputs/repo-overlay" / SPEC
    assert sha(spec_src) == SPEC_SHA, "overlay spec sha mismatch"
    for rep in reps:
        run = f"{os.environ.get('PN_PREFIX', 'o2')}-r{rep}" if stratum == "sonnet" else f"{os.environ.get('PN_PREFIX', 'o2')}h-r{rep}"
        d = run_dir(run)
        if d.exists():
            print("skip existing", run)
            continue
        (d / "home/.claude/rules/prompts").mkdir(parents=True)
        shutil.copytree(S1 / "inputs/repo-overlay", d / "ws")
        (d / "ws" / D / "review").mkdir(parents=True, exist_ok=True)
        (d / "ws" / D / "specs/history").mkdir(parents=True, exist_ok=True)
        assert sha(d / "ws" / SPEC) == SPEC_SHA
        (d / "command.md").write_text(cmd)
        (d / "home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules_txt)
        st = new_state(run, stratum, rep)
        for kind, fname in (("first", "panel.json"), ("re-review", "panel-rr.json")):
            out = cli("panel", "resolve", *PANEL_ARGS, "--run-id", run, "--kind", kind).stdout
            (d / fname).write_text(out)
            st["panel" if kind == "first" else "panel_rr"] = json.loads(out)
        save(run, st)
        print("built", run)


def extend():
    """D4: add three Sonnet replicates, once, and only if the Sonnet n=6 result is INCONCLUSIVE."""
    r = rules()
    e = r["extension"]
    res = compute_results()
    son = res["sonnet"]
    marker = AB / "extension.json"
    if marker.exists():
        print("REFUSED: the extension was already done once; a second one needs the owner (D4)")
        return 1
    if not A.extension_needed(son["class"], son["n_total"], r):
        print(f"REFUSED: extension applies only when the Sonnet n={e['base_replicates']} result is INCONCLUSIVE "
              f"(now: {son['class']['decision']}, n={son['n_total']})")
        return 1
    start = e["base_replicates"] + 1
    build("sonnet", list(range(start, start + e["extra_replicates"])))
    marker.write_text(json.dumps({"at": now(), "from": start, "n": e["extra_replicates"], "reason": son["class"]["reasons"]}))
    print("extension created; run advance.py until complete, then analyze with n=9 (final)")
    return 0


# ---------------------------------------------------------------- prompts and sandboxes
def make_prompt(run, key, sb, text):
    p = run_dir(run) / f"PROMPT-{key}.md"
    p.write_text(text)
    return p


def prep_reviewer(run, n, rid):
    d = run_dir(run)
    sb = d / f"r{n}-{rid}"
    if sb.exists():
        shutil.rmtree(sb)
    (sb / "home/.claude/rules/prompts").mkdir(parents=True)
    shutil.copytree(S1 / "inputs/repo-overlay", sb / "ws")
    (sb / "ws" / D / "review").mkdir(parents=True, exist_ok=True)
    (sb / "ws" / D / "specs/history").mkdir(parents=True, exist_ok=True)
    shutil.copy(d / "command.md", sb / "command.md")
    shutil.copy(d / "home/.claude/rules/prompts/document_review_loop_prompts.md", sb / "home/.claude/rules/prompts/document_review_loop_prompts.md")
    shutil.copy(ws(run) / SPEC, sb / "ws" / SPEC)
    out = f"{D}/review/round{n}.md"
    if n == 1:
        b = brief("R1", out=out)
    else:
        base = f"{D}/specs/history/spec-v{n - 1}.md"
        prior = f"{D}/review/round{n - 1}.md"
        shutil.copy(ws(run) / base, sb / "ws" / base)
        shutil.copy(ws(run) / prior, sb / "ws" / prior)
        b = brief(f"R{n}", out=out, prior=prior, base=base)
    text = WRAP.format(sb=sb, wsdir="ws", cmdpart=CMDPART.format(sb=sb), brief=b)
    return make_prompt(run, f"R{n}.{rid}", sb, text), sb / "ws" / out


def prep_revise(run, n, ids):
    d = run_dir(run)
    shutil.copy(ws(run) / SPEC, ws(run) / D / f"specs/history/spec-v{n}.md")
    b = brief(f"V{n}", out=f"{D}/review/revise{n}.md", rep=f"{D}/review/round{n}.md", ids=ids)
    text = WRAP.format(sb=d, wsdir="ws", cmdpart="", brief=b)
    return make_prompt(run, f"V{n}", d, text), ws(run) / D / f"review/revise{n}.md"


def prep_audit(run, k):
    """C9.2: fresh sandbox aud / aud2 = overlay + the run's final spec + frozen command + frozen rules file."""
    name = "aud" if k == 1 else "aud2"
    ad = run_dir(run) / name
    if ad.exists():
        shutil.rmtree(ad)
    (ad / "home/.claude/rules/prompts").mkdir(parents=True)
    shutil.copytree(S1 / "inputs/repo-overlay", ad / "ws")
    (ad / "ws" / D / "review").mkdir(parents=True, exist_ok=True)
    shutil.copy(ws(run) / SPEC, ad / "ws" / SPEC)
    cmd = git_show(BASE_REF, CMD_REL)
    assert hashlib.sha256(cmd.encode()).hexdigest() == AUD_CMD_SHA
    frozen = (P11 / "rules.md").read_text()
    assert hashlib.sha256(frozen.encode()).hexdigest() == AUD_RULES_SHA
    (ad / "command.md").write_text(cmd)
    (ad / "home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(frozen)
    text = WRAP.format(sb=ad, wsdir="ws", cmdpart=CMDPART.format(sb=ad), brief=aud_brief())
    key = "AUD" if k == 1 else "AUD2"
    return make_prompt(run, key, ad, text), ad / "ws" / AUD_OUT


def prep_adj(run, st):
    d = run_dir(run)
    led = json.loads((ws(run) / D / "review/ledger.json").read_text())
    rows = list(led["rows"])
    order = list(range(len(rows)))
    random.Random(run).shuffle(order)
    sbx = d / "adj"
    if sbx.exists():
        shutil.rmtree(sbx)
    (sbx / "home").mkdir(parents=True)
    shutil.copytree(S1 / "inputs/repo-overlay", sbx / "ws")
    (sbx / "ws" / D / "review").mkdir(parents=True, exist_ok=True)
    mapping, parts = {}, []
    for k, idx in enumerate(order, 1):
        row = rows[idx]
        mapping[f"X{k}"] = row["lid"]
        lines = [f"### X{k}", "", f"- anchor: {json.dumps(row['anchor'], ensure_ascii=False)}"]
        if row.get("anchor2"):
            lines.append(f"- anchor2: {json.dumps(row['anchor2'], ensure_ascii=False)}")
        lines.append(f"- refs: {', '.join(row.get('refs') or []) or '-'}")
        lines.append(f"- claim: {row.get('claim', '')}")
        parts.append("\n".join(lines))
    (sbx / "ws" / D / "review/adj-input.md").write_text("# Findings to adjudicate\n\n" + "\n\n".join(parts) + "\n")
    (d / "adj-map.json").write_text(json.dumps(mapping, indent=1))
    text = WRAP.format(sb=sbx, wsdir="ws", cmdpart="", brief=ADJ_BRIEF)
    return make_prompt(run, "ADJ", sbx, text), sbx / "ws" / D / "review/adj.md"


# ---------------------------------------------------------------- models
def alias_for(run, key):
    st = load(run)
    r = rules()
    haiku = st["stratum"] == "haiku"
    hm = r["strata"]["haiku_model"]
    if key.startswith("AUD"):
        return r["strata"]["audit_model"]              # D3: the frozen audit is always Sonnet
    if key == "ADJ":
        return hm if haiku else "sonnet"   # OWNER RULE: Fable/Tier 0 never used; ADJ runs on Sonnet in these arms
    if key.startswith("V"):
        return hm if haiku else "sonnet"
    m = re.match(r"R(\d)\.(.+)$", key)
    n, rid = int(m.group(1)), m.group(2)
    if n >= 2 and haiku:
        return hm                                       # D3: re-reviewers run on Haiku in the Haiku stratum
    return reviewer_row(st, n, rid)["launch"]


EXPECTED_MODEL = {"sonnet": "sonnet", "haiku": "haiku", "opus": "opus"}


# ---------------------------------------------------------------- done detection and ingest
def out_path(run, key):
    d = run_dir(run)
    m = re.match(r"R(\d)\.(.+)$", key)
    if m:
        return d / f"r{m.group(1)}-{m.group(2)}" / "ws" / D / f"review/round{m.group(1)}.md"
    if key == "ADJ":
        return d / "adj/ws" / D / "review/adj.md"
    if key == "AUD":
        return d / "aud/ws" / AUD_OUT
    if key == "AUD2":
        return d / "aud2/ws" / AUD_OUT
    if key.startswith("V"):
        return ws(run) / D / f"review/revise{key[1:]}.md"
    raise KeyError(key)


def prompt_path(run, key):
    return run_dir(run) / f"PROMPT-{key}.md"


def step_done(run, key, st, say=print):
    """Done when the output exists and the transcript shows SubagentHandback/DONE, or no transcript exists and the output has not changed for SETTLE_S."""
    out = out_path(run, key)
    info = st["launched"].get(key, {})
    hits = A.find_transcripts(prompt_path(run, key), TASKS_GLOB)
    if hits:
        stats = [A.transcript_stats(h) for h in hits]
        if out.exists() and any(s["done"] for s in stats):
            return True
        if not out.exists() and any(s["done"] for s in stats):
            return True            # worker ended without writing: ingest records the missing report
        return False
    if out.exists():
        return (time.time() - out.stat().st_mtime) >= SETTLE_S
    t = info.get("t_epoch")
    if t and time.time() - t > STALE_S:
        say(f"WARN stale: {run} {key} has no output {int((time.time() - t) / 60)} min after launch (still waiting; nothing is stopped)")
    return False


def token_info(run, key, alias):
    exp = EXPECTED_MODEL.get(alias, alias)
    s = A.step_tokens(prompt_path(run, key), TASKS_GLOB, exp)
    if not s:
        return {"out": None, "model": None, "wall_s": None, "in": None, "cache_read": None, "cache_write": None}
    return {"out": s["out"], "model": s["model"], "wall_s": A.wall_seconds(s["t0"], s["t1"]), "in": s["in"],
            "cache_read": s["cache_read"], "cache_write": s["cache_write"]}


def verdict_of(text):
    vs = re.findall(r"verdict:\s*\**\s*(PASS|FAIL|INCOMPLETE)", text, re.I)
    return vs[-1].upper() if vs else "NONE"


def ingest_reviewer(run, key, st, say=print):
    m = re.match(r"R(\d)\.(.+)$", key)
    n, rid = int(m.group(1)), m.group(2)
    out = out_path(run, key)
    alias = st["launched"][key]["alias"]
    tok = token_info(run, key, alias)
    text = out.read_text(errors="ignore") if out.exists() else ""
    v = verdict_of(text) if text else "NONE"
    if (not out.exists()) or v in ("INCOMPLETE", "NONE"):
        if st["retries"].get(key, 0) < RETRIES:
            st["retries"][key] = st["retries"].get(key, 0) + 1
            say(f"MANUAL: {run} {key} verdict {v} / report {'missing' if not out.exists() else 'present'}: relaunching once")
            unlaunch_state(run, key, st)
        else:
            say(f"MANUAL: {run} {key} still {v} after the relaunch: marked lost")
            st["lost"].append(key)
        return
    shutil.copy(out, ws(run) / D / f"review/round{n}-{rid}.md")
    parsed = findings_mod().parse_block(text)
    sev = collections.Counter(f["severity"] for f in parsed["findings"])
    tv = json.loads(cli("telemetry", "taskvars", out.parents[3] / SPEC, "--specialization", "software-spec",
                        "--kind", "first" if n == 1 else "re-review").stdout)
    st["log"][key] = {"verdict": v, "block_ok": parsed["ok"], "findings": len(parsed["findings"]),
                      "blocking": sum(1 for f in parsed["findings"] if f["blocking"]),
                      "by_severity": {k: sev.get(k, 0) for k in ("CRITICAL", "MAJOR", "MINOR")},
                      "errors": parsed["errors"][:5], "tokens": tok, "task": tv, "alias": alias,
                      "report_bytes": len(text.encode())}
    st["done"].append(key)


def ingest_simple(run, key, st, say=print):
    out = out_path(run, key)
    alias = st["launched"][key]["alias"]
    tok = token_info(run, key, alias)
    rec = {"output_exists": out.exists(), "tokens": tok, "alias": alias}
    if out.exists():
        t = out.read_text(errors="ignore")
        rec["report_bytes"] = len(t.encode())
        if key.startswith("AUD"):
            rec["verdict"] = verdict_of(t)
            rec["blocking_ids"] = c93.parse_ids(c93.ids_from(out)) if rec["verdict"] == "FAIL" else []
            rec["blocking_tags"] = [list(x) for x in c93.blocking_tags(out)]
            rec["spec_audited"] = {"bytes": len((out.parents[3] / SPEC).read_bytes())}
        if key.startswith("V"):
            rec["spec_after"] = spec_stats(ws(run))
    if not out.exists():
        if st["retries"].get(key, 0) < RETRIES:
            st["retries"][key] = st["retries"].get(key, 0) + 1
            say(f"MANUAL: {run} {key} produced no output: relaunching once")
            unlaunch_state(run, key, st)
            return
        say(f"MANUAL: {run} {key} produced no output after the relaunch: marked lost")
        st["lost"].append(key)
        return
    st["log"][key] = rec
    st["done"].append(key)


def unlaunch_state(run, key, st):
    st["launched"].pop(key, None)
    try:
        out_path(run, key).unlink()
    except (FileNotFoundError, KeyError):
        pass


def unlaunch(run, key):
    st = load(run)
    unlaunch_state(run, key, st)
    st["done"] = [k for k in st["done"] if k != key]
    st["lost"] = [k for k in st["lost"] if k != key]
    save(run, st)
    print("unlaunched", run, key)


# ---------------------------------------------------------------- merge, revise, telemetry
def run_merge(run, n, st, say=print):
    rids = reviewers_of(st, n)
    use = [r for r in rids if f"R{n}.{r}" in st["done"]]
    rd = ws(run) / D / "review"
    res_file = run_dir(run) / ("panel.json" if n == 1 else "panel-rr.json")
    args = ["merge", "--ledger", rd / "ledger.json", "--doc", ws(run) / SPEC, "--round", n, "--resolution", res_file, "--out", rd / f"round{n}.md"]
    for r in use:
        args += ["--report", f"{r}={rd / f'round{n}-{r}.md'}"]
    out = json.loads(cli(*args).stdout)
    st["log"][f"M{n}"] = out
    append_telemetry(run, n, st, use, out)
    return out


def append_telemetry(run, n, st, used, merged):
    pr = st["panel"] if n == 1 else st["panel_rr"]
    for rid in used:
        key = f"R{n}.{rid}"
        lg = st["log"][key]
        row = reviewer_row(st, n, rid)
        haiku_override = st["stratum"] == "haiku" and n >= 2
        resolved = "claude-haiku-5-5" if haiku_override else row["model"]
        rec = {"schema_version": "review-telemetry/1", "kind": "reviewer_run", "record_id": __import__("uuid").uuid4().hex, "ts_utc": now(),
               "run_id": run, "step": f"R{n}", "round": n, "reviewer_id": rid,
               "panel": {"template_id": pr["template_id"], "template_version": pr["template_version"], "template_sha256": pr["template_sha256"],
                         "tiers_version": pr["tiers_version"], "tiers_sha256": pr["tiers_sha256"], "environment": pr["environment"],
                         "panel_size": len(pr["reviewers"])},
               "slot": {"slot_id": row["slot_id"], "tier": row["tier"], "alias": row["alias"], "strategy": row["strategy"], "seed": row["seed"],
                        "fallback_depth": row["fallback_depth"], "stand_in": True if haiku_override else row["stand_in"]},
               "model": {"resolved": resolved, "launch": lg["alias"], "observed": lg["tokens"]["model"]},
               "task": lg["task"],
               "output": {"block_ok": lg["block_ok"], "findings": lg["findings"], "blocking": lg["blocking"], "by_severity": lg["by_severity"],
                          "verdict": lg["verdict"], "verdict_mismatch": lg["verdict"] != merged["verdict"]},
               "cost": {"tokens_in": lg["tokens"]["in"], "tokens_cache_read": lg["tokens"]["cache_read"],
                        "tokens_cache_write": lg["tokens"]["cache_write"], "tokens_out": lg["tokens"]["out"], "wall_s": lg["tokens"]["wall_s"]},
               "context": {"experiment": "pn1", "arm": DESIGN, "replicate": st["rep"], "stratum": st["stratum"]},
               "stratum": st["stratum"]}
        f = run_dir(run) / f"telemetry-{key}.json"
        f.write_text(json.dumps(rec))
        cli("telemetry", "append", "--dir", TELEMETRY_DIR, "--record", f)
        st["telemetry_ids"][key] = rec["record_id"]


def run_ledger_revise(run, n, st):
    rd = ws(run) / D / "review"
    out = json.loads(cli("ledger", "revise", "--ledger", rd / "ledger.json", "--old", ws(run) / D / f"specs/history/spec-v{n}.md",
                         "--new", ws(run) / SPEC, "--fixmap", rd / f"revise{n}.md").stdout)
    st["log"][f"L{n}"] = out


# ---------------------------------------------------------------- the per-run state machine
def advance_run(run, say=print, dry_run=False):
    """Progress one run as far as scripts allow. Returns [(key, alias, prompt_path)] for workers that must be launched."""
    st = load(run)
    wants = []
    changed = False
    while True:
        progress = False
        if st["phase"] in ("lost", "complete"):
            break
        # ---- ADJ runs in parallel with V1 once M1 exists
        if "M1" in st["log"] and "ADJ" not in st["done"] and "ADJ" not in st["lost"]:
            if "ADJ" not in st["launched"]:
                if not dry_run:
                    p, _ = prep_adj(run, st)
                else:
                    p = prompt_path(run, "ADJ")
                wants.append(("ADJ", alias_for(run, "ADJ"), p))
            elif step_done(run, "ADJ", st, say):
                if dry_run:
                    say(f"DRYRUN would ingest {run} ADJ")
                else:
                    ingest_simple(run, "ADJ", st, say)
                    progress = changed = True
        n = st["round"]
        if st["phase"] == "review":
            rids = reviewers_of(st, n)
            pending = False
            for rid in rids:
                key = f"R{n}.{rid}"
                if key in st["done"] or key in st["lost"]:
                    continue
                if key not in st["launched"]:
                    if dry_run:
                        p = prompt_path(run, key)
                    else:
                        p, _ = prep_reviewer(run, n, rid)
                    wants.append((key, alias_for(run, key), p))
                    pending = True
                elif step_done(run, key, st, say):
                    if dry_run:
                        say(f"DRYRUN would ingest {run} {key}")
                        pending = True
                    else:
                        ingest_reviewer(run, key, st, say)
                        progress = changed = True
                        pending = pending or (key not in st["done"] and key not in st["lost"])
                else:
                    pending = True
            if not pending and not dry_run:
                # every reviewer of the round is ingested or lost
                lost = [k for k in st["lost"] if k.startswith(f"R{n}.")]
                good = [r for r in rids if f"R{n}.{r}" in st["done"]]
                if len(lost) >= 2 or not good:
                    say(f"MANUAL: {run} round {n}: {len(lost)} reviewer(s) lost: run marked lost")
                    st["phase"] = "lost"
                    changed = True
                    break
                if not any(st["log"][f"R{n}.{r}"]["block_ok"] for r in good):
                    for r in good:
                        k = f"R{n}.{r}"
                        if st["retries"].get(k, 0) < RETRIES:
                            st["retries"][k] = st["retries"].get(k, 0) + 1
                            say(f"MANUAL: {run} {k}: no reviewer's findings block parsed; relaunching it once")
                            st["done"].remove(k)
                            unlaunch_state(run, k, st)
                            progress = changed = True
                    if progress:
                        continue
                merged = run_merge(run, n, st, say)
                st["phase"] = "merged"
                progress = changed = True
        elif st["phase"] == "merged":
            m = st["log"][f"M{n}"]
            if m["decision"] in ("PASS", "ESCALATE"):
                st["phase"] = "audit"
                progress = changed = True
            else:
                key = f"V{n}"
                if key in st["done"]:
                    if not dry_run:
                        run_ledger_revise(run, n, st)
                        st["round"] = n + 1
                        st["phase"] = "review"
                        progress = changed = True
                elif key in st["lost"]:
                    st["phase"] = "lost"
                    changed = True
                    break
                elif key not in st["launched"]:
                    if dry_run:
                        p = prompt_path(run, key)
                    else:
                        p, _ = prep_revise(run, n, ", ".join(m["brief_ids"]))
                    wants.append((key, alias_for(run, key), p))
                elif step_done(run, key, st, say):
                    if dry_run:
                        say(f"DRYRUN would ingest {run} {key}")
                    else:
                        ingest_simple(run, key, st, say)
                        progress = changed = True
        elif st["phase"] == "audit":
            pend = False
            for k, key in ((1, "AUD"), (2, "AUD2")):
                if key in st["done"] or key in st["lost"]:
                    continue
                if key not in st["launched"]:
                    if dry_run:
                        p = prompt_path(run, key)
                    else:
                        p, _ = prep_audit(run, k)
                    wants.append((key, alias_for(run, key), p))
                    pend = True
                elif step_done(run, key, st, say):
                    if dry_run:
                        say(f"DRYRUN would ingest {run} {key}")
                        pend = True
                    else:
                        ingest_simple(run, key, st, say)
                        progress = changed = True
                        pend = pend or (key not in st["done"] and key not in st["lost"])
                else:
                    pend = True
            adj_open = "M1" in st["log"] and "ADJ" not in st["done"] and "ADJ" not in st["lost"]
            if not pend and not adj_open:
                st["phase"] = "complete"
                st["final"] = final_record(run, st)
                progress = changed = True
        if not progress:
            break
    if changed and not dry_run:
        save(run, st)
    return wants


def final_record(run, st):
    rounds = [int(k[1:]) for k in st["log"] if re.fullmatch(r"M\d", k)]
    last = st["log"][f"M{max(rounds)}"]
    sp = spec_stats(ws(run))
    return {"reviews": max(rounds), "decision": last["decision"], "final_bytes": sp["bytes"], "final_sha256": sp["sha256"],
            "growth": sp["bytes"] / 57763 - 1}


# ---------------------------------------------------------------- results (shared by analyze and extend)
def run_summary(run):
    st = load(run)
    r = rules()
    f = st.get("final")
    out = {"run": run, "stratum": st["stratum"], "phase": st["phase"], "lost": st["lost"]}
    if st["phase"] != "complete" or not f:
        return out
    loop_keys = [k for k in st["log"] if re.match(r"(R\d\.|V\d$|ADJ$)", k)]
    toks = {k: (st["log"][k].get("tokens") or {}).get("out") for k in loop_keys}
    A_incl = sum(v or 0 for v in toks.values())
    A_excl = sum(v or 0 for k, v in toks.items() if k != "ADJ")
    aud = [(st["log"].get(k) or {}) for k in ("AUD", "AUD2")]
    aud_tok = (aud[0].get("tokens") or {}).get("out")
    blk = [len(a.get("blocking_ids") or []) if a.get("verdict") == "FAIL" else 0 for a in aud]
    rev_logs = [st["log"][k] for k in loop_keys if k.startswith("R")]
    out.update({"reviews": f["reviews"], "decision": f["decision"], "pass": f["decision"] == "PASS", "final_bytes": f["final_bytes"],
                "growth": f["growth"], "A": A_incl, "A_excl_adj": A_excl, "AUD_tok": aud_tok, "tokens_by_step": toks,
                "audit_blocking": blk, "audit_ids": [a.get("blocking_ids") for a in aud], "audit_tags": [a.get("blocking_tags") for a in aud],
                "residual": sum(blk) / 2, "block_ok": [x["block_ok"] for x in rev_logs],
                "events": events_of(st), "lost_reviewers": [k for k in st["lost"]]})
    return out


def events_of(st):
    ev = collections.Counter()
    for k, v in st["log"].items():
        if re.fullmatch(r"M\d", k):
            ev["regressed"] += len(v.get("regressed", []))
            ev["cleared"] += len(v.get("cleared", []))
            ev["refound"] += len(v.get("refound", []))
        if re.fullmatch(r"L\d", k):
            ev["named_not_touched"] += len(v.get("named_not_touched", []))
            ev["rejected"] += len(v.get("rejected", []))
    return dict(ev)


def load_haiku_baseline(path=None):
    """Tolerant reader of the coordinator's results.json. Returns {'n', 'mean_blk', 'lost_rate', 'runs'} or None."""
    p = pathlib.Path(path or rules()["haiku"]["baseline_results"])
    if not p.exists():
        return None
    try:
        d = json.loads(p.read_text())
    except Exception:
        return None
    runs = d.get("runs", d) if isinstance(d, dict) else d
    if isinstance(runs, dict):
        runs = [dict(v, run=k) for k, v in runs.items() if isinstance(v, dict)]
    blk, lost = [], 0
    for r in runs:
        b = r.get("audit_blocking", r.get("aud_blocking", r.get("blocking", r.get("blk"))))
        if isinstance(b, (list, tuple)) and b:
            blk.append(sum(b) / len(b))
        elif isinstance(b, (int, float)):
            blk.append(float(b))
        else:
            lost += 1
    if not runs:
        return None
    return {"n": len(runs), "mean_blk": A.mean(blk), "lost_rate": lost / len(runs), "runs": runs}


def compute_results():
    r = rules()
    res = {}
    for stratum in ("sonnet", "haiku"):
        runs = [run_summary(x) for x in all_runs({stratum})]
        done = [x for x in runs if "reviews" in x]
        n_total = len(done)
        stats = None
        if done:
            audits = [b for x in done for b in x["audit_blocking"]]
            aud1 = A.mean(x["audit_blocking"][0] for x in done)
            aud2 = A.mean(x["audit_blocking"][1] for x in done)
            bo = [b for x in done for b in x["block_ok"]]
            tv = A.token_view([x["A"] for x in done], [x["AUD_tok"] or 0 for x in done], r)
            stats = {"BLK_T": A.mean(audits), "PASS_T": sum(1 for x in done if x["pass"]) / len(done), "GROWTH_T": A.mean(x["growth"] for x in done),
                     "R_LOOP": tv["R_LOOP"], "R_B": tv["R_B"], "BLOCK_OK": (sum(bo) / len(bo)) if bo else 0.0, "completed": len(done),
                     "audit_gap": abs(aud1 - aud2), "AUD1": aud1, "AUD2": aud2, "tokens": tv}
        res[stratum] = {"runs": runs, "done": done, "n_total": n_total, "stats": stats,
                        "lost_rate": (len(runs) - len(done)) / len(runs) if runs else 0.0}
    son = res["sonnet"]
    son["class"] = A.classify(son["stats"], r) if son["stats"] else {"decision": "INCONCLUSIVE", "cost_hold": False, "reasons": ["no completed Sonnet runs"]}
    hk = res["haiku"]
    hk_test = {"n": hk["n_total"], "mean_blk": hk["stats"]["BLK_T"] if hk["stats"] else None, "lost_rate": hk["lost_rate"]}
    base = load_haiku_baseline()
    hk["gate"] = A.haiku_gate(hk_test if hk["stats"] else None, base, r)
    hk["baseline"] = base
    res["final"] = A.final_decision(son["class"], hk["gate"])
    return res


# ---------------------------------------------------------------- commands
def status():
    for run in all_runs():
        st = load(run)
        pend = [k for k in st["launched"] if k not in st["done"] and k not in st["lost"]]
        extra = ""
        if st.get("final"):
            extra = f" | reviews {st['final']['reviews']} {st['final']['decision']} bytes {st['final']['final_bytes']}"
        print(f"{run} [{st['stratum']}] round {st['round']} phase {st['phase']} done {len(st['done'])} lost {len(st['lost'])} running {pend}{extra}")


def basetokens():
    loops, auds = [], []
    for r in range(1, 7):
        run = f"a3-r{r}"
        steps = {}
        for stp in ("R1", "V1", "R2", "V2", "R3", "AUD"):
            p = P11 / "runs" / run / f"PROMPT-{stp}.md"
            if p.exists():
                s = A.step_tokens(p, TASKS_GLOB, "sonnet")
                steps[stp] = s["out"] if s else None
        loop = sum(v or 0 for k, v in steps.items() if k != "AUD")
        print(run, steps, "loop", loop, "audit", steps.get("AUD"))
        loops.append(loop)
        auds.append(steps.get("AUD") or 0)
    a, u = sum(loops) / len(loops), sum(auds) / len(auds)
    print(f"A_BASE (loop-only mean) {a:.0f} | one audit {u:.0f} | B_TOK = B_BASE (loop + one audit) {a + u:.0f}")
    return a, u


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "status"
    if c == "build":
        stratum = sys.argv[sys.argv.index("--stratum") + 1] if "--stratum" in sys.argv else "sonnet"
        build(stratum)
    elif c == "extend":
        sys.exit(extend())
    elif c == "status":
        status()
    elif c == "unlaunch":
        unlaunch(sys.argv[2], sys.argv[3])
    elif c == "basetokens":
        basetokens()
    elif c in ("outcomes", "analyze"):
        import report
        getattr(report, c)()
    else:
        print(__doc__)
