#!/usr/bin/env python3
"""A/B harness ab5 (design d5): requirements-lint pre-pass, the PN1 four-reviewer panel as the first review (R1.t1b-1 Sonnet with the
ab4 acceptance-criteria sweep, R1.t2-1 / R1.t3-1 / R1.t4-1 Haiku stand-ins; one reviewer per tier, owner correction 2026-11-10), deterministic MERGE over the four reports with cleaned
finding blocks, PN1's adjudication worker ADJ (measurement only), cleaned verify gate VF1-VF3, revise V1/V2, scoped re-reviews R2/R3
with lint, frozen audits AUD/AUD2 (always Sonnet).

Derived from $SP/p16/ab4/harness.py (copied, then modified where marked "ab5"). From PN1 ($SP/p13/ab1/harness.py): the panel
resolution (pn1_panel.py, byte copy of the product resolver, run with the frozen template + tier table), the reviewer ids and sandbox
names r1-<rid>, the ADJ brief (verbatim), the ADJ input shuffle (random.Random(run)), the ADJ / reviewer models (alias_for), and the
lost-reviewer rule (one lost reviewer: merge the other three; two lost: the run is lost).

Usage (run with `python3 harness.py ...`):
  build [--stratum sonnet|haiku] [--extend]     create sandboxes (d5-r1..r6 | haiku refused in ab5 | d5-r7..r9)
  prep RUN STEP [K=V ...]                      write RUN/PROMPT-STEP.md (R1.<rid>/R2/R3 also run the lint: lint-1/2/3.md)
  ingest RUN STEP                              record outputs of a finished step
  setids RUN STEP "F1, F2"                     manual blocking ids for a report
  unlaunch RUN STEP                            drop a launch ledger entry (relaunch once; then the reviewer / run is lost)
  status | tokens [RUN] | basetokens | analyze
Cost rule (owner decision D6): nothing here stops, skips or truncates a run because of token cost.
Cost is evaluated only in `analyze`, after runs are complete."""
import collections
import datetime
import hashlib
import importlib.util
import json
import os
import pathlib
import random
import re
import shutil
import sys
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_themes as sc  # noqa: E402
from score_themes import ids_from, parse_ids, blocking_findings, clean_body  # noqa: E402,F401
import reqlint as L  # noqa: E402
import full  # noqa: E402  (variant `full`: PN1 ledger merge / revise / re-review, see full.py)

S = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f")
SP = S / "scratchpad"
P11 = SP / "p11"
AB = pathlib.Path(os.environ.get("AB5_DIR") or (SP / "p18" / "ab5"))
RUNS = AB / "runs"
FROZEN = AB / "frozen"                      # no git access: command, rules and panel data are frozen copies, hash-pinned in decision.json
TASKS_GLOB = os.environ.get("AB_TASKS_GLOB", "/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output")
DESIGN = "d5"
SPEC_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
S1 = SP / "exp346/.dev/experiments/346-validation/phase2/S1"
D = ".dev/orca-command-refactor"
SPEC = f"{D}/specs/orca-worker-contract-spec.md"
HIST = f"{D}/specs/history"
REVIEW = f"{D}/review"
FLAGS = "--mode critique --focus requirements,architecture"
AUD_OUT = f"{D}/review/audit.md"
# ab5: the PN1 panel. Reviewer ids come from the resolution (asserted equal to this list at build time).
PANEL_RIDS = ["t1b-1", "t2-1", "t3-1", "t4-1"]     # ab5 template: one reviewer per tier (owner correction 2026-11-10)
R1S = [f"R1.{r}" for r in PANEL_RIDS]
STEPS = R1S + ["ADJ", "VF1", "V1", "R2", "VF2", "V2", "R3", "VF3", "AUD", "AUD2"]
LOOP_STEPS = [s for s in STEPS if s not in ("AUD", "AUD2")]
OUT = {**{s: f"{REVIEW}/round1.md" for s in R1S}, "ADJ": f"{REVIEW}/adj.md",
       "VF1": f"{REVIEW}/verify-1.md", "V1": f"{REVIEW}/revise1.md", "R2": f"{REVIEW}/round2.md",
       "VF2": f"{REVIEW}/verify-2.md", "V2": f"{REVIEW}/revise2.md", "R3": f"{REVIEW}/round3.md",
       "VF3": f"{REVIEW}/verify-3.md", "AUD": AUD_OUT, "AUD2": AUD_OUT}
VERIFY_BLOCK = ("> verification (coordinator, VERIFY step VF{n}; verifier reply " + REVIEW + "/verify-{n}.md): "
                "confirmed blocking ids: {c}. Rejected, kept as noted, unactioned and not prior blocking findings for the next "
                "re-review: {r}. The Reviser brief below is narrowed to the confirmed ids.")
REVISER_RULES = ("Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; "
                 "add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; "
                 "prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.")
NUMWORD = {1: "one", 2: "two", 3: "three", 4: "four"}


def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
def run_dir(run): return RUNS / run
def arm_of(run): return 3
def load(run): return json.load(open(run_dir(run) / "state.json"))
def ws(run): return run_dir(run) / "ws"
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def sha_text(t): return hashlib.sha256(t.encode()).hexdigest()
def all_runs(): return sorted((p.name for p in RUNS.iterdir() if (p / "state.json").exists()), key=run_sort) if RUNS.exists() else []
def decision(): return json.load(open(AB / "decision.json"))
def is_r1(step): return step.startswith("R1.")
def rid_of(step): return step.split(".", 1)[1]
def max_runs(): return int(os.environ.get("AB_MAX") or decision()["MAX_CONCURRENT_RUNS"])


def save(run, st):
    tmp = run_dir(run) / "state.json.tmp"            # atomic write (PN1 save)
    json.dump(st, open(tmp, "w"), indent=1)
    tmp.replace(run_dir(run) / "state.json")


def run_sort(run):
    m = re.match(r"d5(f?)(h?)-r(\d+)$", run)
    # stratum, then replicate, then variant: the two arms interleave (d5-r1, d5f-r1, d5-r2, ...) so both get slots at the same time
    return (1 if m and m.group(2) else 0, int(m.group(3)) if m else 0, 1 if m and m.group(1) else 0)


def variant_of(st): return st.get("variant", "panel")
def is_full(st): return variant_of(st) == "full"


def forbidden(model):
    """OWNER RULE: Fable (Tier 0) is forbidden everywhere; ab5 uses no Opus step. True when a model id / alias / tier name matches."""
    m = str(model or "").lower()
    return any(p in m for p in decision()["FORBIDDEN_MODELS"]["patterns"])


def frozen(name, sha_key):
    """A frozen input file, checked against the sha256 pinned in decision.json (no git needed)."""
    text = (FROZEN / name).read_text()
    assert sha_text(text) == decision()["frozen"][sha_key], f"frozen file {name} does not match decision.json {sha_key}"
    return text


def spec_stats(base):
    b = (pathlib.Path(base) / SPEC).read_bytes()
    return {"bytes": len(b), "lines": b.count(b"\n"), "sha256": hashlib.sha256(b).hexdigest()}


def section(text, title):
    m = re.search(rf"^### {re.escape(title)}\n(.*?)(?=^### |^## |\Z)", text, re.S | re.M)
    return m.group(1).strip()


# ---------------------------------------------------------------- PN1 panel (ab5)
_PANEL = None


def panel_mod():
    """The PN1 product resolver (byte copy pn1_panel.py, standard library only), hash-checked, loaded by path."""
    global _PANEL
    if _PANEL is None:
        p = HERE / "pn1_panel.py"
        assert sha(p) == decision()["frozen"]["panel_code_sha"], "pn1_panel.py does not match decision.json panel_code_sha"
        spec = importlib.util.spec_from_file_location("pn1_panel", p)
        _PANEL = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_PANEL)
    return _PANEL


def resolve_panel(run, kind, template=None, sha_key="panel_template_sha"):
    """= PN1 `superclaude review panel resolve --env anthropic-only --run-id RUN --kind KIND` (PN1 code and tier table) with the ab5
    template (t1b, t2, t3, t4); template="review-panel.default.json", sha_key="pn1_panel_template_sha" gives PN1's own panel."""
    tpl = json.loads(frozen(template or decision()["panel"]["template"], sha_key))
    tiers = json.loads(frozen("review-tiers.default.json", "panel_tiers_sha"))
    return apply_model_map(panel_mod().resolve(tpl, tiers, decision()["panel"]["environment"], run, kind))


def apply_model_map(res, dec=None):
    """OWNER 2026-11-10: reviewer models by gateway alias. reviewer_models.stand_in true (mock): keep PN1's resolution (t2/t3 Haiku
    stand-ins, stand_in=true) and record live_model / live_name from live_alias_map; false (live): model, model_name and launch come
    from live_alias_map[alias] and stand_in=false. Only these fields change; no model name lives in code."""
    dec = dec or decision()
    amap, mock = dec["live_alias_map"], dec["reviewer_models"]["stand_in"]
    out = json.loads(json.dumps(res))
    for r in out["reviewers"]:
        live = amap[r["alias"]]
        r["live_model"], r["live_name"] = live["model"], live["name"]
        if not mock:
            r["model"], r["model_name"], r["launch"], r["stand_in"] = live["model"], live["name"], live["launch"], False
    return out


def reviewer_row(st, rid):
    return next(r for r in st["panel"]["reviewers"] if r["reviewer_id"] == rid)


def r1_steps(st):
    return [f"R1.{r['reviewer_id']}" for r in st["panel"]["reviewers"]]


# ---------------------------------------------------------------- build
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


def run_names(stratum, extend, variant="panel"):
    pre = decision()["variants"][variant]["prefix"]
    if stratum == "haiku":
        return [f"{pre}h-r{i}" for i in range(1, decision()["N_HAIKU"] + 1)]
    if extend:
        n = decision()["N_SONNET"]
        return [f"{pre}-r{i}" for i in range(n + 1, n + decision()["N_EXTEND"] + 1)]
    return [f"{pre}-r{i}" for i in range(1, decision()["N_SONNET"] + 1)]


def build(stratum="sonnet", extend=False, variant="panel"):
    if variant not in decision()["variants"]:
        raise SystemExit(f"unknown variant {variant} (panel | full)")
    pre = decision()["variants"][variant]["prefix"]
    if stratum == "haiku" and not decision().get("HAIKU_ENABLED"):
        raise SystemExit("build --stratum haiku refused: ab5 builds the Sonnet stratum only (BRIEF; decision.json HAIKU_ENABLED is false). "
                         "The Haiku code path (d5h-r1..r4, Haiku loop / re-review models, analysis) is kept; set HAIKU_ENABLED to build it.")
    if extend:
        if stratum != "sonnet":
            raise SystemExit("--extend is Sonnet only")
        mp = AB / "metrics.json"
        m = json.load(open(mp)) if mp.exists() else {}
        sm = m.get(variant, {}).get("sonnet", {})
        if not (sm.get("n_runs") == decision()["N_SONNET"] and sm.get("extension_eligible")):
            raise SystemExit("--extend refused: metrics.json does not record a Sonnet n=6 outcome of INCONCLUSIVE")
        if (RUNS / f"{pre}-r{decision()['N_SONNET'] + 1}").exists():
            raise SystemExit("--extend refused: already extended once (never extend twice without the owner)")
    cmd = frozen("command.md", "cmd_sha")
    vc = decision()["variants"][variant]
    rules = frozen(vc["rules"], vc["rules_sha"])
    RUNS.mkdir(parents=True, exist_ok=True)
    for run in run_names(stratum, extend, variant):
        d = run_dir(run)
        if d.exists():
            print("skip existing", run)
            continue
        panel = resolve_panel(run, "first")
        panel_rr = resolve_panel(run, "re-review")
        assert [r["reviewer_id"] for r in panel["reviewers"]] == PANEL_RIDS == decision()["panel"]["reviewers"], panel["reviewers"]
        assert [r["reviewer_id"] for r in panel_rr["reviewers"]] == ["t1b-1"], panel_rr["reviewers"]
        for r in panel["reviewers"] + panel_rr["reviewers"]:
            assert not any(forbidden(r.get(k)) for k in ("model", "launch", "alias", "tier", "model_name")), f"forbidden model in panel: {r}"
            assert r["stand_in"] == (r["model"] != r["live_model"]), f"stand_in flag inconsistent with live_alias_map: {r}"
        sandbox(d, d, cmd, rules)
        for rid in PANEL_RIDS:
            sandbox(d / f"r1-{rid}", d, cmd, rules)
        (d / "panel.json").write_text(json.dumps(panel, indent=1))
        (d / "panel-rr.json").write_text(json.dumps(panel_rr, indent=1))
        st = {"run": run, "design": DESIGN, "variant": variant, "rep": int(run.split("-r")[1]), "stratum": stratum, "loop_model": stratum,
              "frozen": decision()["frozen"], "cmd_sha": sha_text(cmd), "rules_sha": sha_text(rules),
              "panel": panel, "panel_rr": panel_rr, "sweep_reviewer": decision()["panel"]["sweep_reviewer"],
              "done": [], "prepared": [], "transitioned": [], "log": {}, "launched": {}, "noted_unactioned": [],
              "loop_end": None, "manual": [], "relaunch": {}, "lost": False, "complete": False, "merge": {},
              "r1_lost": [], "adj_lost": False}
        st["models"] = {s: expected_model(st, s) for s in STEPS}
        save(run, st)
    print("built", sorted(p.name for p in RUNS.iterdir()))


# ---------------------------------------------------------------- briefs (arm-3 strings, unchanged from Stage 2 / ab4)
CTX = (f"First read {D}/README.md (binding shared context; the files under {D}/inventory/ are the only evidence you can check, "
       f"mark any citation you cannot check UNVERIFIED). Cite path:line for every claim. Write only your output file(s).")
RULES_PTR = "~/.claude/rules/prompts/document_review_loop_prompts.md"


SWEEP = ("In addition, check every acceptance criterion and every live-check step one by one: for each, state whether it can pass as written "
         "for every command and phase it covers, and record any that cannot as a finding under the same blocking rule.")


def lint_rel(n): return f"{REVIEW}/lint-{n}.md"


def brief_first(out, sweep=False):
    """Panel reviewer brief: the PN1 / ab1 first-review brief plus the PN2 lint value (= ab4 R1a). sweep=True (t1b-1 only): plus the
    ab4 R1b sentence."""
    b = f"Run /sc:spec-panel @{SPEC} {FLAGS} . Review per the FIRST-REVIEW prompt in {RULES_PTR}. Values: candidate={SPEC}, lint={lint_rel(1)}."
    if sweep:
        b += " " + SWEEP
    return b + f"\nWrite the full report to {out}. Do not edit anything else. {CTX}"


def brief_re(prior, base, out, n):
    return (f"Run /sc:spec-panel @{SPEC} {FLAGS} --re-review {prior} --baseline {base} . Re-review per the RE-REVIEW prompt in {RULES_PTR}. "
            f"Values: candidate={SPEC}, baseline={base}, prior={prior}, lint={lint_rel(n)}.\nWrite the full report to {out}. Do not edit anything else. {CTX}")


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


# PN1 ADJ_BRIEF, verbatim ($SP/p13/ab1/harness.py)
ADJ_BRIEF = ("Read .dev/orca-command-refactor/README.md and the spec .dev/orca-command-refactor/specs/orca-worker-contract-spec.md. "
             "For each finding X<k> in .dev/orca-command-refactor/review/adj-input.md decide whether it is a real defect that blocks implementation: "
             "write the sentence \"An implementer who follows the stated text as written builds X, and X is wrong because Y.\" and confirm it only if "
             "that sentence holds with no further assumption. Write .dev/orca-command-refactor/review/adj.md ending with a fenced block with info string "
             "adj-v1 holding one JSON line per finding: {\"x\": \"X1\", \"verdict\": \"confirmed\" or \"rejected\" or \"unsure\", \"reason\": \"<one sentence>\"}. "
             "Do not edit anything else.")


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
    if is_r1(step):
        return ws(run) / REVIEW / f"round1-{rid_of(step)}.md"
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


# ---------------------------------------------------------------- findings lists (ab4 item 4a, unchanged)
def check_findings_text(text):
    """Lines of a verifier / adjudicator finding list that must not be there: banner / non-finding section lines, Reviser-brief notes,
    recommendation / option / priority / origin lines. [] when the list holds only finding sections."""
    bad = []
    for ln in text.splitlines():
        if sc.BANNER_RE.match(ln) or sc.CUT_RE.match(ln) or sc.DROP_RE.match(ln):
            bad.append(ln)
    return bad


def findings_text(run, n):
    """Finding list for VF{n}, n >= 2 (n == 1 is written by merge). Finding sections only: each finding is cut at the first
    banner / non-finding section and its advice lines are dropped (ab4 item 4a)."""
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
        heading, body = sc.finding_block(text, fid, clean=True)
        if heading is None:
            hits = [ln for ln in text.splitlines() if re.search(rf"(?<![\w-]){re.escape(fid)}(?![\w-])", ln)]
            hits = [ln for ln in clean_body(hits) if not (sc.BANNER_RE.match(ln) or sc.CUT_RE.match(ln))][:10]
            parts.append(f"### {fid}\n" + "\n".join(hits))
            continue
        lines = [heading] + (body or "").splitlines()
        if not (body or "").strip() and n > 1 and prev is not None:
            h2, b2 = sc.finding_block(prev, fid, clean=True)
            if h2 is not None:
                lines += ["(text of this finding in the prior report)", h2] + (b2 or "").splitlines()
        parts.append(f"### {fid}\n" + "\n".join(lines))
    out = "\n\n".join(parts)
    bad = check_findings_text(out)
    if bad:
        raise ValueError(f"finding list for VF{n} still carries non-finding lines: {bad[:3]}")
    (ws(run) / REVIEW / f"findings-{n}.md").write_text(out + "\n")
    return out, ids


def verify_brief_text(findings):
    rules = frozen("rules.md", "rules_sha")
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
    cmd = frozen("command.md", "aud_cmd_sha")                # the audit command is the product command (same sha): frozen instrument
    rules = frozen("audit-rules.md", "aud_rules_sha")
    (ad / "command.md").write_text(cmd)
    (ad / "home/.claude/rules/prompts/document_review_loop_prompts.md").write_text(rules)
    text = wrap(ad, audit_brief(), True)
    p = d / ("PROMPT-AUD.md" if k == 1 else "PROMPT-AUD2.md")
    p.write_text(text)
    return p


def run_lint(run, n):
    """Deterministic lint step (no model): lint-<n>.md for the candidate as it is now (PN2 lint, code copied to reqlint.py).
    lint-1 is also placed in each panel reviewer's sandbox. Recorded in state['log']['LINT<n>']; never counted as a loop step."""
    cfg = decision()["lint"]
    data = (ws(run) / SPEC).read_bytes()
    checks = L.parse_checks(cfg["checks"])
    result = L.run_lint(data, checks)
    text = L.render_md(result)
    out = ws(run) / lint_rel(n)
    out.write_text(text, encoding="utf-8")
    st = load(run)
    if n == 1:
        for rid in [r["reviewer_id"] for r in st["panel"]["reviewers"]]:
            q = run_dir(run) / f"r1-{rid}" / "ws" / lint_rel(1)
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_text(text, encoding="utf-8")
    st["log"][f"LINT{n}"] = {"checks": list(checks), "findings": len(result["findings"]),
                             "by_check": dict(collections.Counter(f["check"] for f in result["findings"])),
                             "ids": [f["lint_id"] for f in result["findings"]], "sha256": sha_text(text),
                             "spec_sha256": hashlib.sha256(data).hexdigest(), "stratum": st["stratum"]}
    save(run, st)
    return result


def mark_prepared(run, step):
    st = load(run)
    if step not in st["prepared"]:
        st["prepared"].append(step)
    save(run, st)


def adj_input(run):
    """ab5 ADJ input: the merged findings (cleaned blocks of findings-1.md), each Mn relabelled X<k> in PN1's shuffled order
    (random.Random(run)); the sub-entry source lines (reviewer + id) are dropped so the adjudicator is blind to tier and reviewer."""
    st = load(run)
    text = (ws(run) / REVIEW / "findings-1.md").read_text()
    blocks = {}
    for m in re.finditer(r"(?ms)^### (M\d+)\n(.*?)(?=^### M\d+\n|\Z)", text):
        blocks[m.group(1)] = m.group(2).strip("\n")
    mids = [g["mid"] for g in st["merge"]["groups"]]
    assert set(blocks) == set(mids), (sorted(blocks), mids)
    order = list(range(len(mids)))
    random.Random(run).shuffle(order)
    mapping, parts = {}, []
    for k, idx in enumerate(order, 1):
        mid = mids[idx]
        x = f"X{k}"
        mapping[x] = mid
        body = re.sub(rf"(?m)^#### {mid}\.([a-z]) \([^)\n]*\)$", rf"#### {x}.\1", blocks[mid])
        parts.append(f"### {x}\n{body}")
    out = "# Findings to adjudicate\n\n" + "\n\n".join(parts) + "\n"
    bad = check_findings_text(out)
    if bad:
        raise ValueError(f"ADJ input still carries non-finding lines: {bad[:3]}")
    if re.search(r"(?m)^#{3,4} M\d+\b", out) or "round1-t" in out:
        raise ValueError("ADJ input leaks a merged id or a reviewer source")
    return out, mapping


def prep_adj(run):
    d = run_dir(run)
    out, mapping = adj_input(run)
    sbx = d / "adj"
    if sbx.exists():
        shutil.rmtree(sbx)
    (sbx / "home").mkdir(parents=True)
    shutil.copytree(S1 / "inputs/repo-overlay", sbx / "ws")
    (sbx / "ws" / D / "review").mkdir(parents=True, exist_ok=True)
    shutil.copy(ws(run) / SPEC, sbx / "ws" / SPEC)          # the reviewed candidate (== overlay spec before V1, as in PN1)
    (sbx / "ws" / REVIEW / "adj-input.md").write_text(out)
    (d / "adj-map.json").write_text(json.dumps(mapping, indent=1))
    p = d / "PROMPT-ADJ.md"
    p.write_text(wrap(sbx, ADJ_BRIEF, False))
    st = load(run)
    st["log"].setdefault("ADJ", {})["map"] = mapping
    save(run, st)
    return p


def prep(run, step, subs=None):
    subs = subs or {}
    d = run_dir(run)
    st = load(run)
    if step in ("AUD", "AUD2"):
        p = prep_audit(run, 1 if step == "AUD" else 2)
    elif is_r1(step):
        rid = rid_of(step)
        sb = d / f"r1-{rid}"
        run_lint(run, 1)
        p = d / f"PROMPT-{step}.md"
        p.write_text(wrap(sb, brief_first(OUT[step], sweep=(rid == st["sweep_reviewer"])), True))
    elif step == "ADJ":
        p = full.prep_adj(run) if is_full(st) else prep_adj(run)
    elif step.startswith("VF"):
        n = int(step[2])
        if is_full(st):
            findings, ids = full.vf_findings(run, n)
        elif n == 1:
            findings = (ws(run) / REVIEW / "findings-1.md").read_text().rstrip("\n")
            bad = check_findings_text(findings)
            if bad:
                raise ValueError(f"merged finding list for VF1 still carries non-finding lines: {bad[:3]}")
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
        run_lint(run, n)                       # lint of the revised candidate, as it is now
        p = d / f"PROMPT-{step}.md"
        if is_full(st):
            p.write_text(full.prep_rereview(run, n))          # PN1 prep_reviewer sandbox r<n>-t1b-1 + ab4 brief_re (lint value)
        else:
            p.write_text(wrap(d, brief_re(prior, base, OUT[step], n), True))
    else:
        raise ValueError(step)
    mark_prepared(run, step)
    print(p)
    return p


# ---------------------------------------------------------------- merge (ab4 merge generalised to the panel's reports)
def merge_header(st, n_reports):
    return f"# Merged first review (coordinator; MERGE rule over {NUMWORD.get(n_reports, n_reports)} independent first reviews of the review panel)"


def merge(run):
    """Deterministic MERGE of the panel's first reviews (every reviewer that was not lost). Returns the merged ids ([] if no blocking item)."""
    st = load(run)
    R = ws(run) / REVIEW
    items = []
    reviewers = {}
    used = [s for s in r1_steps(st) if s not in st.get("r1_lost", [])]
    for step in used:
        rid = rid_of(step)
        p = R / f"round1-{rid}.md"
        t = p.read_text(errors="ignore")
        v = sc.verdict_of(t)
        fs = blocking_findings(p, manual_ids(st, step), cut=True)    # cut: a finding ends at the first banner / non-finding section
        row = reviewer_row(st, rid)
        reviewers[rid] = {"verdict": v, "sha256": sha(p), "ids": [f["id"] for f in fs], "themes": [f["theme"] for f in fs],
                          "tier": row["tier"], "model": expected_model(st, step)}
        for f in fs:
            items.append(dict(f, src=f"round1-{rid}.md"))
    spec_sha = sha(ws(run) / SPEC)
    head = ["review: 1 of 3", "", merge_header(st, len(used)), "", f"candidate: {SPEC} sha256 {spec_sha}", "", "sources:"]
    srcs = [f"- {REVIEW}/round1-{rid}.md verdict {reviewers[rid]['verdict']} sha256 {reviewers[rid]['sha256']}" for rid in reviewers]
    lost = [rid_of(s) for s in st.get("r1_lost", [])]
    if lost:
        srcs.append(f"- lost panel reviewer(s), not merged: {', '.join(lost)}")
    if not items:
        (R / "round1.md").write_text("\n".join(head + srcs + ["", "No report has a blocking finding.", "", "verdict: PASS", ""]))
        st["merge"] = {"raw_count": 0, "merged_count": 0, "groups": [], "reviewers": reviewers, "lost": lost, "done": True,
                       "stratum": st["stratum"]}
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
    st["merge"] = {"raw_count": len(items), "merged_count": len(groups), "groups": gl, "reviewers": reviewers, "lost": lost, "done": True,
                   "stratum": st["stratum"]}
    st.setdefault("log", {}).setdefault("VF1", {})["finding_ids"] = [g["mid"] for g in gl]
    save(run, st)
    return [g["mid"] for g in gl]


def strip_heading(h):
    return re.sub(r"^\s*(?:#+\s*)?(?:[-*]\s*)?(?:\*\*)?", "", h or "").strip()


def member_section(run, member):
    src, fid = member.split("/", 1)
    t = (ws(run) / REVIEW / src).read_text(errors="ignore")
    h, b = sc.finding_block(t, fid)
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


def reconcile_confirmed(table, ids, text):
    """The verifier's own final `confirmed:` line is authoritative when an id has several table rows (sub-entries Mn.a, Mn.b: the
    first row may say reject while a later one holds). Pure function; returns a new table. No `confirmed:` line: table unchanged."""
    table = dict(table)
    cl = re.findall(r"(?im)^\W*confirmed:\s*(.+)$", text)
    if cl:
        named = set(re.findall(r"\b[A-Z]{1,2}-?\d+\b", cl[-1])) if not re.match(r"(?i)\W*none\b", cl[-1]) else set()
        for i in ids:
            if i in named and table[i][0] != "confirm":
                table[i] = ("confirm", "confirmed via the verifier's confirmed line (another row for this id holds)")
            elif i not in named and table[i][0] == "confirm":
                table[i] = ("reject", table[i][1] + " [not on the verifier's confirmed line]")
    return table


def ingest_vf(run, st, n, outp):
    text = outp.read_text(errors="ignore")
    R = ws(run) / REVIEW
    ids = st["log"].get(f"VF{n}", {}).get("finding_ids") or []
    table, ok = parse_verify(text, ids)
    print(f"  verify table {run} VF{n} parse_ok={ok}")
    for fid in ids:
        print(f"   {fid}: {table[fid][0]} ({table[fid][1][:100]})")
    # fix 2026-11-10 (b1h-r3 clean VF1): one id can have several rows (sub-entries Mn.a, Mn.b); the verifier's own
    # final `confirmed:` line is authoritative when present (it names Mn when any sub-entry holds).
    table = reconcile_confirmed(table, ids, text)
    confirmed = [i for i in ids if table[i][0] == "confirm"]
    rejected = {i: table[i][1] for i in ids if table[i][0] == "reject"}
    shutil.copy(outp, R / f"verify-{n}.md")
    c_txt = ", ".join(confirmed) or "none"
    r_txt = "; ".join(f"{i} (verifier: {r})" for i, r in rejected.items()) or "none"
    block = VERIFY_BLOCK.format(n=n, c=c_txt, r=r_txt)
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
        revs = st["merge"]["reviewers"]
        rep = ["review: 1 of 3", "", merge_header(st, len(revs)), "",
               f"candidate: {SPEC} sha256 {sha(ws(run) / SPEC)}", "", "sources:"]
        rep += [f"- {REVIEW}/round1-{rid}.md verdict {revs[rid]['verdict']} sha256 {revs[rid]['sha256']}" for rid in revs]
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
        rep += ["## Follow-up candidates", "", f"Listed in the {NUMWORD.get(len(revs), len(revs))} source reports above; not merged.", "",
                "## Reviser brief", "",
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
    return {"finding_ids": ids, "confirmed": confirmed, "rejected": rejected, "parse_ok": ok}


def parse_adj(text, mapping):
    """PN1 ADJ reply: JSON lines {"x": "X1", "verdict": ..., "reason": ...} (adj-v1 block), parsed as PN1 report.truth_adjudicated does.
    -> ({Mn: (verdict, reason)}, parse_ok)."""
    out = {}
    for ln in text.splitlines():
        ln = ln.strip()
        if ln.startswith("{") and '"x"' in ln:
            try:
                d = json.loads(ln)
            except Exception:
                continue
            mid = mapping.get(d.get("x"))
            if mid:
                out[mid] = (str(d.get("verdict", "")).lower(), d.get("reason", ""))
    return out, set(out) == set(mapping.values()) and bool(mapping)


# ---------------------------------------------------------------- ingest
def out_path(run, step):
    d = run_dir(run)
    if step in ("R2", "R3") and is_full(load(run)):
        return d / f"r{step[1]}-t1b-1" / "ws" / OUT[step]          # PN1 re-review sandbox
    if is_r1(step):
        return d / f"r1-{rid_of(step)}" / "ws" / OUT[step]
    if step == "ADJ":
        return d / "adj" / "ws" / OUT[step]
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
    for k in ("output_tokens", "finding_ids", "map"):
        if k in old:
            rec[k] = old[k]
    if outp.exists():
        t = outp.read_text(errors="ignore")
        rec["report_bytes"] = len(t.encode())
        if is_r1(step) or step in ("R2", "R3", "AUD", "AUD2"):
            rec["verdict"] = sc.verdict_of(t)
            rec["review_header"] = re.findall(r"^\W*review:\s*(\d)\s*of\s*3", t, re.I | re.M)
            rec["labels"] = dict(collections.Counter(re.findall(r"\b(CRITICAL|MAJOR|MINOR)\b", t)))
            rec["blocking_ids"] = ids_from(outp)
            rec["blocking_word_count"] = len(re.findall(r"blocking", t, re.I))
        if is_r1(step):
            shutil.copy(outp, ws(run) / REVIEW / f"round1-{rid_of(step)}.md")
            row = reviewer_row(st, rid_of(step))
            rec["reviewer"] = {k: row[k] for k in ("reviewer_id", "slot_id", "tier", "model", "launch", "stand_in", "seed")}
            rec["sweep"] = rid_of(step) == st["sweep_reviewer"]
        if step in ("R2", "R3") and is_full(st):
            shutil.copy(outp, ws(run) / REVIEW / f"round{step[1]}-t1b-1.md")
        if is_full(st) and (is_r1(step) or step in ("R2", "R3")):
            pb = full.F.parse_block(t)                     # PN1 findings block (the ledger's input); ids_from above is the ab4 cross-check
            rec["block_ok"] = pb["ok"]
            rec["block_findings"] = len(pb["findings"])
            rec["block_blocking"] = [f["id"] for f in pb["findings"] if f["blocking"]]
            rec["block_errors"] = pb["errors"][:5]
        if step == "ADJ":
            table, ok = parse_adj(t, old.get("map") or {})
            rec["verdicts"] = {k: v[0] for k, v in table.items()}
            rec["reasons"] = {k: v[1] for k, v in table.items()}
            rec["parse_ok"] = ok
        if step.startswith("VF"):
            rec.update(full.ingest_vf(run, st, int(step[2]), outp) if is_full(st) else ingest_vf(run, st, int(step[2]), outp))
    if step in ("AUD", "AUD2"):
        base = outp.parents[len(pathlib.PurePosixPath(AUD_OUT).parts) - 1]
        rec["spec_audited"] = {"bytes": (base / SPEC).stat().st_size if (base / SPEC).exists() else None}
    elif not is_r1(step) and not step.startswith("VF") and step != "ADJ":
        rec["spec_after"] = spec_stats(ws(run))
    rec["stratum"] = st["stratum"]                       # D3: every record carries its stratum and model; AUD / AUD2 are always Sonnet
    rec["model"] = expected_model(st, step)
    st["log"][step] = rec
    if step not in st["done"]:
        st["done"].append(step)
    save(run, st)
    print(json.dumps({run: {step: {k: v for k, v in rec.items() if k not in ("labels", "reasons", "map")}}}, indent=1))
    return rec


def unlaunch(run, step, quiet=False):
    """Drop a ledger entry. Second call for the same step: a panel reviewer is lost (the run is lost when a second reviewer is lost,
    PN1 rule); a lost ADJ only marks ADJ lost (measurement device); any other step loses the run (ab4 rule)."""
    st = load(run)
    st["launched"].pop(step, None)
    if step in st["done"]:
        st["done"].remove(step)
    if step in st["transitioned"]:
        st["transitioned"].remove(step)
    keep = {k: v for k, v in st["log"].get(step, {}).items() if k in ("finding_ids", "map")}
    st["log"].pop(step, None)
    if keep:
        st["log"][step] = keep
    n = st["relaunch"].get(step, 0) + 1
    st["relaunch"][step] = n
    outp = out_path(run, step)
    if outp.exists():
        outp.rename(outp.with_name(outp.name + f".failed{n}"))
    if step in ("V1", "V2"):
        snap = ws(run) / HIST / f"spec-v{step[1]}.md"
        if snap.exists():
            shutil.copy(snap, ws(run) / SPEC)
    what = "run"
    if n > 1:
        if is_r1(step):
            if step not in st["r1_lost"]:
                st["r1_lost"].append(step)
            what = f"reviewer {step}"
            if len(st["r1_lost"]) > decision()["panel"]["max_lost_reviewers"]:
                st["lost"] = True
                what = f"reviewer {step}; {len(st['r1_lost'])} panel reviewers lost, run"
        elif step == "ADJ":
            st["adj_lost"] = True
            what = "ADJ (measurement only; the run continues)"
        else:
            st["lost"] = True
    save(run, st)
    if not quiet:
        print((f"LOST {what} " if n > 1 else "unlaunched ") + f"{run} {step}")
    return n


# ---------------------------------------------------------------- transcripts / tokens (ab4 item 5; unchanged except the step-name pattern)
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


OLD_PAT = r"p11/runs/(a3-r\d)/PROMPT-(\w+)\.md"


def norm(s): return " ".join((s or "").split())


SHORT_RE = re.compile(r"Read\s+(\S+?\.md)\s+and\s+follow\s+it\s+exactly", re.I)
STEP_FILE_RE = re.compile(r"PROMPT-([\w.-]+)\.md$")       # ab5: panel step names carry '.' and '-' (R1.t1b-1); ab4 had (\w+)
DIR_STEP = {"adj": "ADJ", "aud": "AUD", "aud2": "AUD2", "vf1": "VF1", "vf2": "VF2", "vf3": "VF3", "r2-t1b-1": "R2", "r3-t1b-1": "R3",
            **{f"r1-{r}": f"R1.{r}" for r in PANEL_RIDS}}


def prompt_table():
    """norm(prompt text) -> (run, step) for every PROMPT-<STEP>.md of every run (misparsed / failed copies excluded)."""
    table = {}
    for run in all_runs():
        for p in sorted(run_dir(run).glob("PROMPT-*.md")):
            if ".misparsed" in p.name or ".failed" in p.name:
                continue
            table[norm(p.read_text(errors="ignore"))] = (run, p.name[len("PROMPT-"):-len(".md")])
    return table


def resolve_short(first, table, runs_dir=None):
    """A short launch message 'Read <abs path>/PROMPT.md and follow it exactly' -> (run, step) by resolving the path:
    a runs/<run>/PROMPT-<STEP>.md path names its key; any other existing file is matched by its text; a <run>/<sandbox dir>/PROMPT.md
    path takes the step from the sandbox directory name (r1-t2-1, adj, vf2, aud ...)."""
    m = SHORT_RE.search(first or "")
    if not m:
        return None
    path = pathlib.Path(m.group(1))
    try:
        path = path.resolve()
    except Exception:
        pass
    rd = pathlib.Path(runs_dir or RUNS).resolve()
    try:
        rel = path.relative_to(rd).parts
    except ValueError:
        rel = None
    if rel and len(rel) == 2 and STEP_FILE_RE.match(rel[1]):
        return (rel[0], STEP_FILE_RE.match(rel[1]).group(1))
    if path.exists():
        k = table.get(norm(path.read_text(errors="ignore")))
        if k:
            return k
    if rel and len(rel) == 3 and rel[2].startswith("PROMPT") and rel[1] in DIR_STEP:
        return (rel[0], DIR_STEP[rel[1]])
    return None


def scan_by_prompt(tasks_glob=None):
    """-> {(run, step): [info, ...]}. The agents are launched with the full prompt pasted, so a transcript is matched to its PROMPT file by
    TEXT: the first user message equals (whitespace-normalised) a PROMPT-<STEP>.md, or contains it, or is the short launch message
    'Read <abs path>/PROMPT.md and follow it exactly' (path resolved). Output tokens: max per message id, each id once (transcript_info)."""
    import glob
    table = prompt_table()
    long_keys = sorted((k for k in table if len(k) >= 200), key=len, reverse=True)
    out = collections.defaultdict(list)
    for f in sorted(glob.glob(tasks_glob or TASKS_GLOB)):
        info = transcript_info(f)
        if not info or not info["first"]:
            continue
        key = norm(info["first"])
        k = table.get(key) or resolve_short(info["first"], table)
        if k is None:
            for pk in long_keys:
                if pk in key:
                    k = table[pk]
                    break
        if k:
            out[k].append(info)
    return out


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
    """Launch alias of a step. AUD/AUD2: always sonnet (D3). R1.<rid>: the PN1 panel resolution's `launch` (t1b-1 sonnet, t2/t3
    haiku stand-ins in anthropic-only; PN1 alias_for keeps the panel models in the Haiku stratum too). ADJ: Sonnet (OWNER RULE; haiku in the
    Haiku stratum). VF / V / R2 / R3: the stratum's loop model (ab4)."""
    if step in ("AUD", "AUD2"):
        m = "sonnet"
    elif is_r1(step):
        m = reviewer_row(st, rid_of(step))["launch"]
    elif step == "ADJ":
        m = decision()["panel"]["adj_model"][st["stratum"]]      # OWNER RULE: Sonnet (PN1 used fable: changed condition)
    else:
        m = st["loop_model"]
    if forbidden(m):
        raise ValueError(f"forbidden model {m!r} for {step} (OWNER RULE: no Fable / Tier 0, no Opus in ab5)")
    return m


def tokens_cmd(only_run=None):
    idx = scan_by_prompt()
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
                st["log"][step]["observed_model"] = best["model"]      # ab5 lanes: the model the transcript actually ran on
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
            if r is None or "output_exists" not in r:
                row.append(f"{s}:-")
            else:
                row.append(f"{s}:{r.get('verdict', 'ok' if r['output_exists'] else 'MISSING')}")
        flag = "LOST" if st["lost"] else ("complete" if st["complete"] else "")
        print(run, st["stratum"], " ".join(row), "| loop_end", st["loop_end"], "| r1_lost", st.get("r1_lost"), flag)


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


STEP_GROUPS = [("panel", lambda s: is_r1(s)), ("merge", lambda s: False), ("ADJ", lambda s: s == "ADJ"),
               ("VF", lambda s: s.startswith("VF")), ("revise", lambda s: s in ("V1", "V2")), ("re-review", lambda s: s in ("R2", "R3"))]


def step_tokens(log):
    return {s: log.get(s, {}).get("output_tokens") for s in STEPS if s in log and "output_exists" in log[s]}


# ---------------------------------------------------------------- lanes (coordinator requirement 2026-11-10; lane map is data in decision.json)
LANE_NAMES = ["primary", "tier234", "audit"]


def slot_of(step):
    """Panel slot of a first-review step: R1.<slot>-<i> -> <slot> (PN1 reviewer_id = slot_id-i). None for other steps."""
    return rid_of(step).rsplit("-", 1)[0] if is_r1(step) else None


def lane_of(step, dec=None):
    lanes = (dec or decision())["lanes"]
    slot = slot_of(step)
    for name in LANE_NAMES:
        ln = lanes.get(name, {})
        if (slot is not None and slot in ln.get("slots", [])) or (slot is None and step in ln.get("steps", [])):
            return name
    return lanes.get("default", "primary")


def lane_label(name, dec, recs=()):
    return dec["lanes"].get("_labels", {}).get(name, name)


def slot_label(rid, dec, recs=()):
    """Per-slot label of the parallel lane: the live model (live_alias_map) next to the model actually used (stand-in or not)."""
    for r in recs:
        for rv in r.get("panel_reviewers", []):
            if rv["reviewer_id"] == rid:
                live = dec["live_alias_map"][rv["alias"]]["name"]
                return f"{rid} live {live}; used {rv['model']}{' (stand-in)' if rv['stand_in'] else ''}"
    return rid


def ledger_models(path=None):
    """{(run, step): model} from the launch ledger (last launch wins)."""
    p = pathlib.Path(path or (AB / "launch-ledger.jsonl"))
    out = {}
    if p.exists():
        for ln in p.read_text().splitlines():
            try:
                d = json.loads(ln)
            except Exception:
                continue
            out[(d.get("run"), d.get("step"))] = d.get("model")
    return out


def step_model(run, st, step, ledger):
    """Resolved model of a step from telemetry: the transcript's observed model when tokens were matched, else the launch-ledger model,
    else the model stamped on the step record at ingest. Never inferred from the step name."""
    rec = st["log"].get(step, {})
    return rec.get("observed_model") or ledger.get((run, step)) or rec.get("model")


def lane_tokens(step_toks, dec=None):
    dec = dec or decision()
    out = {n: 0 for n in LANE_NAMES}
    for s, v in step_toks.items():
        out[lane_of(s, dec)] += v or 0
    out["loop"] = sum(out[n] for n in dec["lanes"]["loop_lanes"])
    out["ADJ"] = step_toks.get("ADJ") or 0                               # visible on its own (inside its lane)
    out["slots"] = {}
    for s, v in step_toks.items():
        if is_r1(s):
            out["slots"][rid_of(s)] = v or 0
    return out


def run_record(run, ov=None, used=None):
    st = load(run)
    log = st["log"]
    dec = decision()
    rec = {"run": run, "stratum": st["stratum"], "lost": st["lost"], "complete": st["complete"], "loop_end": st["loop_end"],
           "relaunched": sum(st["relaunch"].values()) > 0 or bool(st["lost"]), "manual": len(st["manual"]),
           "r1_lost": st.get("r1_lost", []), "adj_lost": st.get("adj_lost", False)}
    rec["rounds"] = 1 + ("R2" in log) + ("R3" in log) if any(r in log for r in R1S) else 0
    rec["agents"] = sum(1 for s in R1S + ["R2", "R3"] if s in log and "output_exists" in log[s])
    rec["lint"] = [log.get(f"LINT{i}", {}).get("findings") for i in (1, 2, 3)]
    rec["lint_by_check"] = [log.get(f"LINT{i}", {}).get("by_check") for i in (1, 2, 3)]
    rec["step_tokens"] = step_tokens(log)
    rec["group_tokens"] = {g: sum(v or 0 for s, v in rec["step_tokens"].items() if f(s)) for g, f in STEP_GROUPS}
    led = ledger_models()
    rec["step_models"] = {s: step_model(run, st, s, led) for s in rec["step_tokens"]}
    rec["panel_reviewers"] = [{k: r.get(k) for k in ("reviewer_id", "alias", "model", "stand_in", "live_model")} for r in st["panel"]["reviewers"]]
    rec["lane_tokens"] = lane_tokens(rec["step_tokens"], dec)
    rec["loop_tokens_incl_adj"] = sum(log.get(s, {}).get("output_tokens", 0) for s in LOOP_STEPS)
    rec["loop_tokens_excl_adj"] = sum(log.get(s, {}).get("output_tokens", 0) for s in LOOP_STEPS if s != "ADJ")
    rec["loop_tokens"] = rec["loop_tokens_incl_adj"] if dec.get("LOOP_INCLUDES_ADJ", True) else rec["loop_tokens_excl_adj"]
    rec["aud_tokens"] = [log.get(s, {}).get("output_tokens") for s in ("AUD", "AUD2")]
    rec["tokens_missing"] = [s for s in LOOP_STEPS if s in log and "output_exists" in log[s] and "output_tokens" not in log[s]]
    fin = st.get("final_spec") or {}
    rec["final_bytes"] = fin.get("bytes")
    rec["final_spec_path"] = str(run_dir(run) / "aud" / "ws" / SPEC)
    rec["audits"] = []
    for step, key in (("AUD", "audit.md"), ("AUD2", "audit2.md")):
        p = out_path(run, step)
        if p.exists() and log.get(step, {}).get("verdict") in ("PASS", "FAIL"):
            fs = score_report(p, f"{run}/{key}", manual_ids(st, step), ov, used)
            rec["audits"].append({"step": step, "verdict": log[step]["verdict"], "findings": fs})
    rec["reviewers"] = {}
    for rid in PANEL_RIDS:
        p = ws(run) / REVIEW / f"round1-{rid}.md"
        if p.exists():
            fs = score_report(p, f"{run}/round1-{rid}.md", manual_ids(st, f"R1.{rid}"), ov, used)
            rec["reviewers"][rid] = {"verdict": sc.verdict_of(p.read_text(errors="ignore")), "findings": fs}
    rec["merge"] = {k: st["merge"].get(k) for k in ("raw_count", "merged_count")}
    rec["vf"] = {s: {k: log[s].get(k) for k in ("finding_ids", "confirmed", "rejected", "parse_ok")} for s in ("VF1", "VF2", "VF3")
                 if s in log and "output_exists" in log[s]}
    rec["adj"] = {k: log["ADJ"].get(k) for k in ("verdicts", "parse_ok")} if "output_exists" in log.get("ADJ", {}) else None
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
    """Pre-registered rules of section 3 on completed Sonnet runs (ab4 decide, unchanged). audit_idx None = pooled, 0/1 = one replica only.
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
            return "ADOPT (Haiku robustness pending)", False, "Haiku stratum not built in ab5 or baseline missing"
        if hk["state"] == "disagrees":
            return "INCONCLUSIVE", False, "Haiku stratum disagrees"
        return "ADOPT", False, ""
    return o, o == "INCONCLUSIVE", ""


def fmt_tok(v): return "-" if v is None else f"{v:,}"


def token_tables(recs):
    """Loop-only output tokens per run and per step (each message id once), grouped so the panel / merge / ADJ / VF / revise / re-review
    costs are visible. merge is a deterministic coordinator step (0 model tokens)."""
    L_ = ["### Loop-only output tokens per run, by step group", "",
          "| run | panel (4 R1) | merge | ADJ | VF | revise | re-review | LOOP incl. ADJ | LOOP excl. ADJ | AUD | AUD2 | missing |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in recs:
        g = r["group_tokens"]
        L_.append(f"| {r['run']}{' LOST' if r['lost'] else ''} | {fmt_tok(g['panel'])} | 0 | {fmt_tok(g['ADJ'])} | {fmt_tok(g['VF'])} | "
                  f"{fmt_tok(g['revise'])} | {fmt_tok(g['re-review'])} | {fmt_tok(r['loop_tokens_incl_adj'])} | {fmt_tok(r['loop_tokens_excl_adj'])} | "
                  f"{fmt_tok(r['aud_tokens'][0])} | {fmt_tok(r['aud_tokens'][1])} | {','.join(r['tokens_missing']) or '-'} |")
    done = [r for r in recs if r["complete"] and not r["lost"]]
    if done:
        mean = {g: sum(r["group_tokens"][g] for r in done) / len(done) for g, _ in STEP_GROUPS}
        L_.append(f"| mean (completed, n={len(done)}) | {mean['panel']:,.0f} | 0 | {mean['ADJ']:,.0f} | {mean['VF']:,.0f} | {mean['revise']:,.0f} | "
                  f"{mean['re-review']:,.0f} | {sum(r['loop_tokens_incl_adj'] for r in done) / len(done):,.0f} | "
                  f"{sum(r['loop_tokens_excl_adj'] for r in done) / len(done):,.0f} | | | |")
    L_ += ["", "### Loop-only output tokens per run, per step (tokens / resolved model)", "", "| run | " + " | ".join(s for s in STEPS) + " |", "|---|" + "---|" * len(STEPS)]
    for r in recs:
        L_.append(f"| {r['run']} | " + " | ".join(f"{fmt_tok(r['step_tokens'].get(s))} / {r['step_models'].get(s) or '?'}" if s in r["step_tokens"] else "." for s in STEPS) + " |")
    L_.append("\n`.` = step not run; `-` = step ran, no transcript matched yet (run `python3 harness.py tokens`). Model = transcript's observed model, "
              "else the launch-ledger model, else the model on the step record (never from the step name). AUD/AUD2 are not loop steps.")
    return "\n".join(L_)


def lane_tables(recs, dec):
    """Loop tokens by lane (decision.json `lanes`), per run and as means; the parallel lane per slot; three headline ratios vs
    FRESH_LOOP_BASE: total loop, primary lane without ADJ, primary lane with ADJ (= primary + adjudicator)."""
    lanes = dec["lanes"]
    base = dec["FRESH_LOOP_BASE"]
    par = [r for r in PANEL_RIDS if lane_of(f"R1.{r}", dec) != "primary"]
    L_ = ["### Lanes", "", "Lane map (decision.json `lanes`): " + "; ".join(
          f"{n} = slots {', '.join(lanes.get(n, {}).get('slots', [])) or '-'} + steps {', '.join(lanes.get(n, {}).get('steps', [])) or '-'}" for n in LANE_NAMES)
          + f"; any other step = {lanes.get('default')}. Loop total = {' + '.join(lanes['loop_lanes'])}; audits are excluded. ADJ (adjudicator, Sonnet) sits in the "
          f"{lane_of('ADJ', dec)} lane and has its own column.", "",
          "| run | " + lane_label("primary", dec) + " | of which ADJ (adjudicator, Sonnet) | " + lane_label("tier234", dec) + " | "
          + " | ".join(slot_label(r, dec, recs) for r in par) + " | LOOP | " + lane_label("audit", dec)
          + " | loop/base | primary excl. ADJ/base | primary + ADJ/base |", "|---|" + "---|" * (8 + len(par))]
    pl = lane_of("ADJ", dec)
    pad = "tier234"

    def row(name, t):
        prim_x = t["primary"] - (t["ADJ"] if pl == "primary" else 0)
        prim_a = prim_x + t["ADJ"]
        return (f"| {name} | {t['primary']:,.0f} | {t['ADJ']:,.0f} | {t[pad]:,.0f} | " + " | ".join(f"{t['slots'].get(r, 0):,.0f}" for r in par)
                + f" | {t['loop']:,.0f} | {t['audit']:,.0f} | {t['loop'] / base:.2f} | {prim_x / base:.2f} | {prim_a / base:.2f} |")
    for r in recs:
        L_.append(row(r["run"] + (" LOST" if r["lost"] else ""), r["lane_tokens"]))
    done = [r for r in recs if r["complete"] and not r["lost"]]
    head = {}
    if done:
        mean = {k: sum(r["lane_tokens"][k] for r in done) / len(done) for k in LANE_NAMES + ["loop", "ADJ"]}
        mean["slots"] = {s: sum(r["lane_tokens"]["slots"].get(s, 0) for r in done) / len(done) for s in PANEL_RIDS}
        L_.append(row(f"**mean (completed, n={len(done)})**", mean))
        px = mean["primary"] - (mean["ADJ"] if pl == "primary" else 0)
        head = {"loop": mean["loop"] / base, "primary": px / base, "primary_adj": (px + mean["ADJ"]) / base}
        L_ += ["", f"Headline ratios vs the fresh-baseline loop ({base:,} tokens), means over completed runs: total loop {head['loop']:.2f}; "
               f"primary lane only (without ADJ) {head['primary']:.2f}; primary + adjudicator {head['primary_adj']:.2f}."]
    else:
        L_ += ["", f"Headline ratios vs the fresh-baseline loop ({base:,} tokens): no completed run yet."]
    return "\n".join(L_), head


def design_tables(recs):
    """Design-specific metrics: per-theme capture of the panel (each reviewer and the union), lint findings, merge, ADJ, verifier."""
    lines = []
    cols = PANEL_RIDS + ["u"]
    dec = decision()
    tot = {x: {t: 0 for t in ("T1", "T2", "T3")} for x in cols}
    ns = 0
    for r in recs:
        th = {x: themes_hit(v["findings"]) for x, v in r["reviewers"].items()}
        if not th:
            continue
        ns += 1
        for t_ in ("T1", "T2", "T3"):
            for x in PANEL_RIDS:
                tot[x][t_] += t_ in th.get(x, set())
            tot["u"][t_] += t_ in set().union(*th.values())
    lines += ["### Per-theme capture, panel (runs with at least one first review)", "",
              "| theme | " + " | ".join(slot_label(x, dec, recs) + (" + AC sweep" if x == dec["panel"]["sweep_reviewer"] else "") for x in PANEL_RIDS)
              + " | union (panel) | baseline k=1 |", "|---|" + "---|" * (len(PANEL_RIDS) + 2)]
    for t_, b in (("T1", "6/6"), ("T2", "2/6"), ("T3", "3/6")):
        lines.append(f"| {t_} | " + " | ".join(f"{tot[x][t_]}/{ns}" for x in cols) + f" | {b} |")
    lines += ["", "| run | " + " | ".join(PANEL_RIDS) + " | union | lost reviewers | lint findings 1/2/3 | lint by check (lint-1) |", "|---|---|---|---|---|---|---|---|---|"]
    for r in recs:
        th = {x: themes_hit(v["findings"]) for x, v in r["reviewers"].items()}
        U = set().union(*th.values()) if th else set()
        cells = [f"{r['reviewers'][x]['verdict']} {len(r['reviewers'][x]['findings'])} {','.join(sorted(th[x])) or '-'}" if x in r["reviewers"] else "-" for x in PANEL_RIDS]
        lt = "/".join("-" if v is None else str(v) for v in r["lint"])
        lines.append(f"| {r['run']} | " + " | ".join(cells) + f" | {','.join(sorted(U)) or '-'} | {','.join(r['r1_lost']) or '-'} | {lt} | {(r['lint_by_check'][0] or {})} |")
    lines += ["", "Cells: verdict, blocking count, themes. t1b-1 carries the ab4 acceptance-criteria sweep sentence; the other three have the plain brief."]
    lines += ["", "### Merged-finding count", "", "| run | raw | merged | dedup ratio |", "|---|---|---|---|"]
    for r in recs:
        raw, mg = r["merge"].get("raw_count"), r["merge"].get("merged_count")
        lines.append(f"| {r['run']} | {raw} | {mg} | {((mg or 0) / raw if raw else 0):.2f} |")
    lines += ["", "### ADJ (PN1 adjudicator, measurement only) vs VF1", "", "| run | merged | ADJ confirmed | rejected | unsure | VF1 confirmed | agree (confirm/other) | parse_ok |", "|---|---|---|---|---|---|---|---|"]
    for r in recs:
        a = r["adj"]
        v1 = r["vf"].get("VF1", {})
        if not a or not a.get("verdicts"):
            lines.append(f"| {r['run']} | {r['merge'].get('merged_count')} | - | - | - | {len(v1.get('confirmed') or [])} | - | {a.get('parse_ok') if a else '-'} |")
            continue
        vs = a["verdicts"]
        conf = set(v1.get("confirmed") or [])
        agree = sum((vs[m] == "confirmed") == (m in conf) for m in vs)
        lines.append(f"| {r['run']} | {len(vs)} | {sum(v == 'confirmed' for v in vs.values())} | {sum(v == 'rejected' for v in vs.values())} | "
                     f"{sum(v == 'unsure' for v in vs.values())} | {len(conf)} | {agree}/{len(vs)} | {a.get('parse_ok')} |")
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


def analyze_variant(variant, dec, base, prov, bnotes):
    used, eyeball = [], []
    recs = {"sonnet": [], "haiku": []}
    for run in all_runs():
        if variant_of(load(run)) != variant:
            continue
        r = run_record(run, None, used)
        recs[r["stratum"]].append(r)
        for a in r["audits"] + [{"step": f"R1.{x}", "findings": v["findings"]} for x, v in r["reviewers"].items()]:
            for f in a["findings"]:
                eyeball.append(f"{run} {a['step']} {f['id']} {f['theme']} :: {(f['heading'] or '')[:100]}")
    S6 = recs["sonnet"]
    n_exp = dec["N_SONNET"] + (dec["N_EXTEND"] if any(r["run"] == f"{dec['variants'][variant]['prefix']}-r{dec['N_SONNET'] + 1}" for r in S6) else 0)
    sonnet = decide(S6, dec, base, n_exp)
    replicas = [decide(S6, dec, base, n_exp, i) for i in (0, 1)]
    hb = haiku_baseline(dec)
    hk = haiku_stratum(recs["haiku"], hb, dec)
    outcome, eligible, note = final_outcome(sonnet, replicas, hk)
    metrics = {"sonnet": dict(sonnet, outcome_final=outcome, n_runs=n_exp, extension_eligible=eligible and n_exp == dec["N_SONNET"], note=note,
                               replicas=[{k: r[k] for k in ("outcome", "BLK_T", "rule")} for r in replicas]),
               "stratum_counts": {k: len(v) for k, v in recs.items()}, "haiku": hk, "baseline": {k: (float(v) if isinstance(v, Fraction) else v) for k, v in base.items()},
               "provisional": prov, "stratum": "sonnet", "variant": variant, "loop_includes_adj": dec.get("LOOP_INCLUDES_ADJ", True),
               "runs": {r["run"]: {"loop_tokens_incl_adj": r["loop_tokens_incl_adj"], "loop_tokens_excl_adj": r["loop_tokens_excl_adj"],
                                   "group_tokens": r["group_tokens"], "step_tokens": r["step_tokens"], "final_spec_path": r["final_spec_path"],
                                   "lane_tokens": r["lane_tokens"], "step_models": r["step_models"],
                                   "audit_blk": [len(a["findings"]) for a in r["audits"]]} for r in S6}}
    T = []
    tag_ = "PROVISIONAL " if prov else ""
    T.append(f"# Variant `{variant}` ({tag_}n={n_exp}; {dec['variants'][variant]['_comment']})\n")
    T.append(f"Outcome: **{outcome}** ({sonnet['rule']}){' - ' + note if note else ''}; R_LOOP {sonnet['R_LOOP']} (decides, limit {dec['rules']['DROP2_RLOOP_LIMIT']}; "
             f"LOOP {'includes' if dec.get('LOOP_INCLUDES_ADJ', True) else 'excludes'} ADJ), R_B {sonnet['R_B']} (reported only)\n")
    T.append(f"Baseline: B_BLK {base['B_BLK']:.2f}, B_AUDFAIL {float(base['B_AUDFAIL']):.3f}, B_THEME {float(base['B_THEME']):.3f} over {base['n_audits']} audits; " + "; ".join(bnotes) + "\n")
    T.append("## Sonnet stratum (" + variant + ")\n\n| run | loop end | rounds / agents | lost reviewers | lint findings 1/2/3 | growth | LOOP | AUD tokens | audit 1 BLK | audit 2 BLK | audit 1 | audit 2 |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in S6:
        au = [f"{a['verdict']} " + ",".join(f"{g['id']}:{g['theme']}" for g in a["findings"]) for a in r["audits"]]
        blk = [str(len(a["findings"])) for a in r["audits"]]
        gr = f"{(r['final_bytes'] - dec['SPEC_BYTES']) / dec['SPEC_BYTES']:+.2%}" if r["final_bytes"] else "-"
        lt = "/".join("-" if v is None else str(v) for v in r["lint"])
        T.append(f"| {r['run']}{' LOST' if r['lost'] else ''} | {r['loop_end']} | {r['rounds']} / {r['agents']} | {','.join(r['r1_lost']) or '-'} | {lt} | {gr} | "
                 f"{r['loop_tokens']} | {r['aud_tokens']} | {blk[0] if blk else '-'} | {blk[1] if len(blk) > 1 else '-'} | {au[0] if au else '-'} | {au[1] if len(au) > 1 else '-'} |")
    T.append("\n## Tokens (loop only; output tokens, each message id once)\n")
    lt, head = lane_tables(S6, dec)
    T.append(lt + "\n")
    T.append(token_tables(S6))
    metrics["lane_headline"] = head
    T.append("\n## Metrics (pooled over completed audits; replicas below)\n")
    for k in ("n_completed", "n_audits", "BLK_T", "audit_fail", "theme_rate", "theme_counts", "loop_pass", "growth", "LOOP_T", "TOK_T", "R_LOOP", "R_B", "REJ1", "N1", "REJ1_rate"):
        T.append(f"- {k}: {sonnet.get(k)}")
    for i, r in enumerate(replicas, 1):
        T.append(f"- replica audit {i} only: {r['outcome']} (BLK_T {r['BLK_T']}, {r['rule']})")
    T.append("\n## Final spec per run (input of the 44-defect ledger scoring)\n")
    for r in S6:
        T.append(f"- {r['run']}: {r['final_spec_path']}{'' if pathlib.Path(r['final_spec_path']).exists() else ' (not yet written)'}")
    T.append("\n## Haiku stratum (never pooled; not built in ab5)\n")
    T.append(json.dumps(hk, indent=1, default=str))
    T.append("\n## Design-specific tables (Sonnet)\n")
    T.append(design_tables(S6))
    T.append("\n## Theme tags to eyeball\n\n" + "\n".join(f"- {e}" for e in eyeball))
    T.append("\n## Theme overrides applied\n\n" + ("\n".join(f"- {u}" for u in sorted(set(used))) or "none"))
    return metrics, T


def analyze():
    dec = decision()
    base, prov, bnotes = baseline_values(dec)
    metrics, T = {}, ["# ab5 RESULTS (two arms from one harness: variant panel = d5-r*, variant full = d5f-r*)\n"]
    for variant in dec["variants"]:
        m, tv = analyze_variant(variant, dec, base, prov, bnotes)
        metrics[variant] = m
        T += tv + [""]
    json.dump(metrics, open(AB / "metrics.json", "w"), indent=1, default=str)
    (AB / "RESULTS.md").write_text("\n".join(T) + "\n")
    print("\n".join(T[:8]))
    return metrics


def main(argv):
    c = argv[1] if len(argv) > 1 else "status"
    if c == "build":
        st = argv[argv.index("--stratum") + 1] if "--stratum" in argv else "sonnet"
        var = argv[argv.index("--variant") + 1] if "--variant" in argv else "panel"
        if st not in ("sonnet", "haiku"):
            raise SystemExit(f"unknown stratum {st}")
        build(st, "--extend" in argv, var)
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
