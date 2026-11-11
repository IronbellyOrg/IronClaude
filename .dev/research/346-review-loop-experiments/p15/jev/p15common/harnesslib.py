"""Reusable parts of $SP/p12/ab2/harness.py and advance.py, parameterized by an ExpConfig (contract J10).

Every user-visible prompt string (WRAP, CMDPART, briefs, audit brief) is byte-identical to p12/ab2, which kept p11 arm 3
byte-for-byte.  D6: nothing in this file reads running token or dollar totals to stop, abort, truncate or skip anything;
cost enters only the post-hoc verdict (analysis.py)."""
import collections
import datetime
import glob as _glob
import hashlib
import json
import os
import pathlib
import re
import shutil
import sys
from dataclasses import dataclass, field

S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S / "scratchpad"
P11 = SP / "p11"
CENTRAL = SP / "central"
S1 = SP / "exp346/.dev/experiments/346-validation/phase2/S1"
FROZEN_CMD_PATH = P11 / "runs/a3-r1/command.md"
FROZEN_RULES_PATH = P11 / "rules.md"
SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
CMD_SHA = "e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494"
RULES_SHA = "3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8"
SPEC_BYTES = 57763
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
AUD_OUT = f"{D}/review/audit.md"
FLAGS = "--mode critique --focus requirements,architecture"
OUT = {3: {"R1": f"{D}/review/round1.md", "V1": f"{D}/review/revise1.md", "R2": f"{D}/review/round2.md",
           "V2": f"{D}/review/revise2.md", "R3": f"{D}/review/round3.md"}}
TASKS_GLOB_DEFAULT = "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output"
QUIET_SECS = 180
STALE_SECS = 60 * 60
PASS_ENDS = ("PASS", "VERIFIED-PASS")


def tasks_glob():
    return os.environ.get("AB_TASKS_GLOB", TASKS_GLOB_DEFAULT)


def max_concurrent_env(default=6):
    return int(os.environ.get("AB_MAX", str(default)))


@dataclass
class ExpConfig:
    root: pathlib.Path                    # experiment dir, e.g. $SP/p15/e3
    design_id: str                        # "p15-E3"
    pattern_root: str                     # regex fragment for transcript matching, e.g. r"p15/e3"
    run_rx: str                           # e.g. r"g3[bc]h?-r\d+"
    decision_path: pathlib.Path
    loop_steps: list                      # all loop steps in canonical order (worker and coordinator steps)
    coordinator_steps: set = field(default_factory=set)   # done in code by advance.py (PK*, J*): never launched, 0 output tokens
    insertion_file: object = None         # rules insertion for test arms (None = frozen rules unchanged)
    insertion_anchor: object = None       # the exact line of the frozen rules file after which the insertion goes
    step_outputs: dict = field(default_factory=dict)       # extra step -> output path relative to the run workspace

    def __post_init__(self):
        self.root = pathlib.Path(self.root)
        self.decision_path = pathlib.Path(self.decision_path)

    @property
    def runs_dir(self):
        return self.root / "runs"

    @property
    def all_steps(self):
        return list(self.loop_steps) + ["AUD", "AUD2"]

    @property
    def worker_loop_steps(self):
        return [s for s in self.loop_steps if s not in self.coordinator_steps]


@dataclass
class RunSpec:
    run: str
    arm: str
    arm_label: str
    stratum: str                  # "sonnet" | "haiku"
    block: int
    block_order: list
    rep: int
    uses_insertion: bool = False
    loop_model: object = None


# ---------------------------------------------------------------- small helpers
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_text(t): return hashlib.sha256(t.encode()).hexdigest()
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def now_iso(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
def run_dir(cfg, run): return cfg.runs_dir / run
def ws(cfg, run): return run_dir(cfg, run) / "ws"
def load(cfg, run): return json.load(open(run_dir(cfg, run) / "state.json"))


def save(cfg, run, st):
    p = run_dir(cfg, run) / "state.json"
    tmp = p.with_name(p.name + ".tmp")
    json.dump(st, open(tmp, "w"), indent=1)
    os.replace(tmp, p)


def run_names(cfg):
    if not cfg.runs_dir.exists():
        return []
    def key(r):
        m = re.search(r"(h?)-r(\d+)$", r)
        return (1 if m and m.group(1) else 0, int(m.group(2)) if m else 0, r)
    return sorted((p.name for p in cfg.runs_dir.iterdir() if (p / "state.json").exists()), key=key)


def loop_model_of(st, step):
    return "sonnet" if step.startswith("AUD") else st["loop_model"]


def spec_stats(cfg, run, base=None):
    b = ((base or ws(cfg, run)) / SPEC).read_bytes()
    return {"bytes": len(b), "lines": b.count(b"\n"), "sha256": hashlib.sha256(b).hexdigest()}


def section(text, title):
    m = re.search(rf"^### {re.escape(title)}\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    return m.group(1).strip()


# ---------------------------------------------------------------- frozen inputs
def frozen_cmd() -> str:
    t = FROZEN_CMD_PATH.read_text()
    assert sha_text(t) == CMD_SHA, "frozen command sha mismatch"
    return t


def frozen_rules() -> str:
    t = FROZEN_RULES_PATH.read_text()
    assert sha_text(t) == RULES_SHA, "frozen rules sha mismatch"
    return t


def insertion_text(cfg) -> str:
    return pathlib.Path(cfg.insertion_file).read_text()


def arm_rules(cfg, arm_uses_insertion: bool) -> str:
    """Frozen rules, or frozen rules with the insertion text on new line(s) immediately after the anchor line."""
    rules = frozen_rules()
    if not arm_uses_insertion:
        return rules
    if cfg.insertion_file is None or cfg.insertion_anchor is None:
        raise ValueError("this experiment has no rules insertion configured")
    lines = rules.split("\n")
    hits = [i for i, ln in enumerate(lines) if ln == cfg.insertion_anchor]
    if len(hits) != 1:
        raise AssertionError(f"insertion anchor occurs {len(hits)} times in the frozen rules (must be exactly once)")
    ins = insertion_text(cfg).rstrip("\n").split("\n")
    return "\n".join(lines[:hits[0] + 1] + ins + lines[hits[0] + 1:])


# ---------------------------------------------------------------- build
def build_runs(cfg, specs):
    """Create sandboxes and p15-run/1 state records.  Existing runs are skipped."""
    cmd = frozen_cmd()
    built = []
    for sp in specs:
        d = run_dir(cfg, sp.run)
        if d.exists():
            print("skip existing", sp.run)
            continue
        rules = arm_rules(cfg, sp.uses_insertion)
        (d / "home/.claude/rules/prompts").mkdir(parents=True)
        shutil.copytree(S1 / "inputs/repo-overlay", d / "ws")
        (d / "ws" / D / "review").mkdir(parents=True)
        (d / "ws" / D / "specs/history").mkdir(parents=True)
        assert sha(d / "ws" / SPEC) == SPEC_SHA, "spec sha mismatch"
        (d / "command.md").write_text(cmd)
        (d / "home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules)
        ins_sha = sha_text(insertion_text(cfg)) if sp.uses_insertion else ""
        model = sp.loop_model or sp.stratum
        save(cfg, sp.run, {
            "schema": "p15-run/1", "run": sp.run, "experiment": cfg.root.name, "design_id": cfg.design_id,
            "arm": sp.arm, "arm_label": sp.arm_label, "stratum": sp.stratum, "loop_model": model,
            "block": sp.block, "block_order": list(sp.block_order), "rep": sp.rep,
            "cmd_sha": sha_text(cmd), "rules_sha": sha_text(rules), "insertion_sha": ins_sha,
            "done": [], "log": {}, "launched": {}, "pending": [], "loop_end": None, "complete": False,
            "lost": False, "lost_reason": None, "manual": [], "manual_ids": {}, "relaunch": {},
            "final_spec": None, "noted_unactioned": [], "eligible": {}, "fallbacks": [],
            "jev": {"logical_calls": 0, "status_counts": {}, "input_tokens": 0, "usd": 0.0}})
        built.append(sp.run)
    print("built", built)
    return built


# ---------------------------------------------------------------- briefs (arm 3 branches kept as in p11/p12)
CTX = (f"First read {D}/README.md (binding shared context; the files under {D}/inventory/ are the only evidence you can check, "
       f"mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file(s).")

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


def new_brief(step, ids=None, out=None, prior=None, base=None, rep=None, values_extra=""):
    """Arm-3 brief of p12/ab2.  `values_extra` (e.g. ", hints=<path>") is appended inside the Values sentence, before its final period."""
    a = 3; spec = SPEC; H = f"{D}/specs/history"
    ctx = CTX
    if step == "R1":
        out = out or OUT[a]["R1"]
        head = f"Run /sc:spec-panel @{spec} {FLAGS} ."
        body = f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={spec}{values_extra}."
        return f"{head} {body}\nWrite the full report to {out}. Do not edit anything else. {ctx}"
    if step in ("R2", "R3"):
        n = 2 if step == "R2" else 3
        prior = prior or OUT[a]["R1" if n == 2 else "R2"]; base = base or f"{H}/spec-v{n-1}.md"
        out = out or OUT[a][step]
        head = f"Run /sc:spec-panel @{spec} {FLAGS} --re-review {prior} --baseline {base} ."
        body = (f"Re-review per the RE-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. "
                f"Values: candidate={spec}, baseline={base}, prior={prior}{values_extra}.")
        return f"{head} {body}\nWrite the full report to {out}. Do not edit anything else. {ctx}"
    if step in ("V1", "V2"):
        n = 1 if step == "V1" else 2
        rep = rep or OUT[a]["R1" if n == 1 else "R2"]; out = out or OUT[a][step]
        vals = {"CANDIDATE": spec, "IDS": ids or "the blocking findings listed in the report"}
        body = (f"Revise per the REVISE prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. "
                f"Values: candidate={spec}, IDS={vals['IDS']}{values_extra}.")
        return (f"{body}\nInputs: the review report {rep} (its Reviser brief lists the blocking ids), the spec, and the files under {D}/inventory/. "
                f"Edit the spec {spec} in place; it is the only file you may change besides your output. Do not run the spec-panel. "
                f"Write {out} with the byte accounting the prompt asks for and one row per finding id (applied where, or rejected with a cited reason). {ctx}")
    raise ValueError(step)


def wrap(sb, brief, with_cmd: bool):
    sb = str(sb)
    return WRAP.format(sb=sb, wsdir="ws", cmdpart=CMDPART.format(sb=sb) if with_cmd else "", brief=brief)


def prep_audit(cfg, run, k):
    """Fresh overlay + the run's final spec + frozen command and rules (sha asserted).  Returns (sandbox, brief, cmdpart)."""
    d = run_dir(cfg, run); sub = "aud" if k == 1 else "aud2"
    ad = d / sub
    if ad.exists():
        shutil.rmtree(ad)
    (ad / "home/.claude/rules/prompts").mkdir(parents=True)
    shutil.copytree(S1 / "inputs/repo-overlay", ad / "ws")
    (ad / "ws" / D / "review").mkdir(parents=True)
    shutil.copy(ws(cfg, run) / SPEC, ad / "ws" / SPEC)
    (ad / "command.md").write_text(frozen_cmd())
    (ad / "home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(frozen_rules())
    brief = (f"Run /sc:spec-panel @{SPEC} {FLAGS} . This is a labelled whole-document audit of the final spec: a first review of the whole document. "
             f"Review per the FIRST-REVIEW prompt in ~/.claude/rules/prompts/document_review_loop_prompts.md. Values: candidate={SPEC}.\n"
             f"Write the full report to {AUD_OUT}. Do not edit anything else. First read {D}/README.md (binding shared context; the files under {D}/inventory/ "
             f"are the only evidence you can check, mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file.")
    return ad, brief, CMDPART


def _sc():
    sys.path.insert(0, str(CENTRAL))
    import score_themes
    return score_themes


def ids_for(cfg, run, n):
    sc = _sc()
    st = load(cfg, run)
    man = st.get("manual_ids", {}).get(f"R{n}")
    if man:
        return sc.parse_ids(man)
    return sc.parse_ids(sc.ids_from(ws(cfg, run) / OUT[3][f"R{n}"]))


DROP_LINE = re.compile(r"(?i)^\s*(?:[-*]\s*)?(?:\*\*)?\s*(recommendation|rationale|experts?|priority|quality impact|why blocking|suggested fix)\b")


def findings(cfg, run, n):
    """The finding list a verifier sees.  Returns (text, ids)."""
    sc = _sc()
    src = (ws(cfg, run) / OUT[3][f"R{n}"]).read_text(errors="ignore")
    ids = ids_for(cfg, run, n)
    parts = []
    for fid in ids:
        heading, body = sc.find_section(src, fid)
        lines = []
        if heading is not None:
            lines = [ln for ln in (body or "").splitlines()]
            if not any(ln.strip() for ln in lines) and n > 1:
                for prev in (f"round{n-1}.orig.md", f"round{n-1}.md"):
                    pp = ws(cfg, run) / D / "review" / prev
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
    return "\n\n".join(parts), ids


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


# ---------------------------------------------------------------- step outputs and ingest
def out_path(cfg, run, step):
    d = run_dir(cfg, run)
    if step == "AUD":
        return d / "aud" / "ws" / AUD_OUT
    if step == "AUD2":
        return d / "aud2" / "ws" / AUD_OUT
    if step.startswith("VF"):
        return d / f"vf{step[2:]}" / "ws" / D / "review" / f"verify-{step[2:]}.md"
    if step in cfg.step_outputs:
        return ws(cfg, run) / cfg.step_outputs[step]
    return ws(cfg, run) / OUT[3][step]


def ingest(cfg, run, step):
    """Record the output of a finished R*/V*/AUD* step (verdict, blockers, spec size)."""
    sc = _sc()
    st = load(cfg, run); outp = out_path(cfg, run, step)
    rec = {"output_exists": outp.exists(), "stratum": st["stratum"], "kind": "worker", "model": loop_model_of(st, step)}
    old = st["log"].get(step, {})
    for k in ("finding_ids", "output_tokens"):
        if k in old:
            rec[k] = old[k]
    if outp.exists():
        t = outp.read_text(errors="ignore"); rec["report_bytes"] = len(t.encode())
        if step in ("R1", "R2", "R3", "AUD", "AUD2"):
            rec["verdict"] = sc.verdict_of(t)
            rec["blocking_ids"] = sc.ids_from(outp)
            rec["blocking"] = ([{"id": f["id"], "heading": f["heading"], "theme": f["theme"], "cited": sorted(f["cited"])}
                                for f in sc.blocking_findings(outp)] if rec["verdict"] == "FAIL" else [])
            if step in ("R1", "R2", "R3"):
                rec["ids"] = ids_for(cfg, run, int(step[1]))
    if step in ("R1", "R2", "R3", "V1", "V2"):
        rec["spec_after"] = spec_stats(cfg, run)
    st = load(cfg, run)
    st["log"][step] = {**st["log"].get(step, {}), **rec}
    if step not in st["done"]:
        st["done"].append(step)
    save(cfg, run, st)
    return rec


def mark_coordinator_done(cfg, run, step, **extra):
    """A step done in code (PK*, J*): 0 output tokens, never launched."""
    st = load(cfg, run)
    st["log"][step] = {**st["log"].get(step, {}), "kind": "coordinator", "output_tokens": 0, "stratum": st["stratum"], **extra}
    if step not in st["done"]:
        st["done"].append(step)
    if step in st["pending"]:
        st["pending"].remove(step)
    save(cfg, run, st)


def requeue(cfg, run, step, reason=""):
    """Drop a launch-ledger entry and re-queue the step; a second time marks the run lost."""
    st = load(cfg, run)
    n = st.setdefault("relaunch", {}).get(step, 0)
    st["launched"].pop(step, None)
    st["log"].pop(step, None)
    if step in st["done"]:
        st["done"].remove(step)
    if n >= 1:
        st["lost"] = True
        st["lost_reason"] = f"{step}: second failure ({reason})"
        st["pending"] = []
        save(cfg, run, st); print(f"LOST {run}: {st['lost_reason']}"); return "lost"
    st["relaunch"][step] = n + 1
    st.setdefault("manual", []).append({"step": step, "relaunch": True, "reason": reason, "time": now_iso()})
    if step not in st["pending"]:
        st["pending"].insert(0, step)
    save(cfg, run, st); print(f"re-queued {run} {step} (relaunch 1 of 1)"); return "requeued"


# ---------------------------------------------------------------- transcripts and tokens
def scan_by_first_message(glob_pat, rx):
    """-> list of (match, info) for every transcript whose first user message matches `rx`.
    info = {file, tokens, models, done}.  Tokens: each message.id counted once (max output_tokens)."""
    found = []
    for f in _glob.glob(glob_pat):
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
            found.append((m, {"file": f, "tokens": sum(per_id.values()), "models": sorted(models), "done": done}))
        except OSError:
            continue
    return found


def scan_transcripts(glob_pat, root_pat, run_rx=r"[\w-]+"):
    """-> {(run, step): [ {file, tokens, models, done} ]}."""
    rx = re.compile(r"^Read \S*?" + root_pat + r"/runs/(?P<run>" + run_rx + r")/PROMPT-(?P<step>\w+)\.md and follow")
    found = collections.defaultdict(list)
    for m, info in scan_by_first_message(glob_pat, rx):
        found[(m.group("run"), m.group("step"))].append(info)
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


def exp_transcripts(cfg):
    return scan_transcripts(tasks_glob(), cfg.pattern_root, cfg.run_rx)


def attach_tokens(cfg):
    """Attach deduplicated output tokens to every worker step; coordinator steps get 0."""
    found = exp_transcripts(cfg)
    for run in run_names(cfg):
        st = load(cfg, run); ch = False
        for step in cfg.all_steps:
            if step in cfg.coordinator_steps:
                if step in st["log"]:
                    st["log"][step]["output_tokens"] = 0; st["log"][step]["kind"] = "coordinator"; ch = True
                continue
            cands = found.get((run, step))
            if not cands:
                continue
            c = pick_transcript(cands, loop_model_of(st, step), key=f"{run} {step}")
            if c is None:
                continue
            rec = st["log"].setdefault(step, {})
            rec["output_tokens"] = c["tokens"]; rec["kind"] = "worker"; rec["model"] = loop_model_of(st, step)
            ch = True
        if ch:
            save(cfg, run, st)
    print("tokens attached")


# ---------------------------------------------------------------- launching and status
def launch_phase(cfg, runs, max_concurrent=None):
    """Print `LAUNCH <abs prompt path> model=<m>` for pending worker steps up to the concurrency cap, in block order
    (Sonnet blocks before Haiku blocks).  Coordinator steps are never launched.  Returns the list of (run, step)."""
    cap = max_concurrent if max_concurrent is not None else max_concurrent_env()
    running = 0
    cand = []
    sts = {r: load(cfg, r) for r in runs}
    for i, run in enumerate(runs):
        st = sts[run]
        if st.get("lost"):
            continue
        running += sum(1 for s in st["launched"] if s not in st["done"])
        for s in st["pending"]:
            if s in cfg.coordinator_steps:
                continue
            order = cfg.all_steps.index(s) if s in cfg.all_steps else len(cfg.all_steps)
            cand.append((1 if st.get("stratum") == "haiku" else 0, st.get("block") or 0, i, order, run, s))
    cand.sort()
    slots = max(0, cap - running)
    launched = []
    for _, _, _, _, run, s in cand[:slots]:
        st = load(cfg, run)
        model = loop_model_of(st, s)
        assert not (s.startswith("AUD") and model != "sonnet"), "Haiku never audits"
        print(f"LAUNCH {run_dir(cfg, run) / ('PROMPT-' + s + '.md')} model={model}")
        st["launched"][s] = now_iso(); st["pending"].remove(s); save(cfg, run, st)
        launched.append((run, s))
    return launched


def status(cfg):
    for run in run_names(cfg):
        st = load(cfg, run); row = []
        for s in cfg.all_steps:
            r = st["log"].get(s)
            if r is None:
                row.append(f"{s}:{'L' if s in st['launched'] else '-'}")
            else:
                row.append(f"{s}:{r.get('verdict', 'ok' if r.get('output_exists', True) else 'MISSING')}")
        flag = "LOST" if st.get("lost") else ("complete" if st.get("complete") else "")
        print(run, st["stratum"], " ".join(row), "| loop_end", st.get("loop_end"), flag)


def telemetry(cfg, run, step, rec):
    """Append one p15-telemetry/1 line (J6) for a finished step."""
    st = load(cfg, run)
    jev = rec.get("jev") or {}
    sc_ = jev.get("status_counts") or {}
    line = {"schema": "p15-telemetry/1", "ts_utc": now_iso(), "experiment": cfg.root.name, "run": run,
            "arm": st.get("arm"), "stratum": st.get("stratum"), "block": st.get("block"), "step": step,
            "kind": "coordinator" if step in cfg.coordinator_steps else "worker",
            "model": None if step in cfg.coordinator_steps else loop_model_of(st, step),
            "output_tokens": rec.get("output_tokens", 0 if step in cfg.coordinator_steps else None),
            "verdict": rec.get("verdict"), "jev_calls": jev.get("calls", sum(sc_.values()) if sc_ else 0),
            "jev_status_counts": sc_, "jev_input_tokens": jev.get("input_tokens", 0),
            "fallback": bool(jev.get("fallback_ids") or rec.get("fallback"))}
    p = cfg.root / "telemetry.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a") as f:
        f.write(json.dumps(line) + "\n")
    return line
