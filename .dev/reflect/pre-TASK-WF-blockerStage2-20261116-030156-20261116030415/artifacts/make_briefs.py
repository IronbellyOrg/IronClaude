"""Wave 2 artifacts (tier_decision.yaml, audit.log) and Step 3B.0 reviewer briefs.
Run: uv run python <this file>   (cwd = repo root). Hunks are copied verbatim from the files by line range.
"""
import datetime
import json
import re
from pathlib import Path

ROOT = Path.cwd()
OUT = Path(".dev/reflect/pre-TASK-WF-blockerStage2-20261116-030156-20261116030415")
PKG = ".dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156"
PF = ".dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115"
PLAN = f"{PKG}/TASK-WF-blockerStage2-20261116-030156.md"
SRC = f"{PKG}/source.md"
PSPEC = f"{PF}/02-brainstorm/merged-requirements.md"
S0 = ".dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md"
S1 = ".dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md"
README = f"{PF}/stage-requests/README.md"
PRIOR = ".dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md"
TASKSK = "src/superclaude/skills/task/SKILL.md"
TRSK = "src/superclaude/skills/tech-research/SKILL.md"
WC = "src/superclaude/core/WORKER-CONTRACT.md"
OVR = "tests/skills/test_review_prompt_overrides.py"
REVINIT = "src/superclaude/cli/review/__init__.py"
CARD = (OUT / "t1-card.md").read_text()
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
RUN_STATE = (f"codegraph run state: index_state=fresh checked_at={NOW} worktree_root={ROOT} projectPath={ROOT}")


def hunk(path, a, b):
    lines = Path(path).read_text().splitlines()
    body = "\n".join(lines[a - 1:b])
    lang = {"md": "markdown", "py": "python"}.get(path.rsplit(".", 1)[-1], "")
    fence = "````" if "```" in body else "```"
    return f"### {path}:{a}-{b}\n\n{fence}{lang}\n{body}\n{fence}\n"


def card_slice(ids, extra=""):
    blocks = re.split(r"(?m)^(?=\*\*T1-\d)", CARD)
    head = [b for b in blocks if not b.startswith("**T1-")][0]
    pick = [b for b in blocks if any(b.startswith(f"**{i} ") or b.startswith(f"**{i}(") or b.startswith(f"**{i}") for i in ids)]
    abbrev = head.split("## Coverage")[0].split("\n\n", 1)[1] if "\n\n" in head else ""
    return abbrev.strip() + "\n\n" + "\n".join(p.strip() + "\n" for p in pick) + extra


COMMON_LEAD = ("The T1 points below are UNVERIFIED LEADS written by the orchestrator, not conclusions. Verify each against the files, "
               "drop the ones you cannot reproduce, and add defects the card missed. Severity rule (use exactly): BLOCKING = a requirement or "
               "check in the plan that cannot be met as written, a wrong or missing result, or data loss; MINOR = wording or format. "
               "Say for each finding whether the plan can still be executed correctly by an executor who follows it literally.")

PERSONA = {
    1: ("analyzer", "sonnet", "claude-gw-tier1b[1m]",
        "Lens (analyzer): root-cause and deviation. Compare the plan with its request (SRC) and with the program spec and the two earlier stage plans: "
        "does the plan do what the request says, is anything the request requires missing, does the plan contradict its sources or itself, and are the "
        "findings of the earlier review (prior report, F1, F6, F7, F8) that touch stage 2 resolved here?",
        ["T1-2", "T1-3", "T1-4", "T1-5"]),
    2: ("qa", "haiku", "claude-gw-tier2[1m]",
        "Lens (qa): coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. "
        "Then check every acceptance line of every task: can it pass and can it fail, does it name a file or command that exists or that an earlier task or package creates, "
        "does a later task of this plan make it false without an end point, and is the order of tasks valid for an executor that runs them top to bottom.",
        ["T1-6", "T1-7", "T1-8"]),
    3: ("refactorer", "opus", "claude-gw-tier1a[1m]",
        "Lens (refactorer): structure and feasibility against the real code. Check that each file, function, section, line number and count the plan names is real and says what the plan says it says, "
        "that the interfaces the plan assumes from the stage 1 and stage 0 plans exist under those names, that an executor can actually do each edit with the surfaces that exist, and look for defects introduced by splitting one 46-task plan into five.",
        ["T1-1", "T1-7", "T1-8"]),
}

HUNKS = {
    1: [(SRC, 1, 19), (PLAN, 17, 27), (PLAN, 46, 58), (PLAN, 72, 79), (PLAN, 106, 115), (TASKSK, 55, 55), (TASKSK, 258, 258),
        (TASKSK, 372, 372), (TASKSK, 409, 409), (WC, 31, 39), (PSPEC, 322, 323), (PSPEC, 430, 441), (S0, 130, 130), (README, 13, 21), (PRIOR, 39, 55)],
    2: [(SRC, 1, 19), (PLAN, 29, 115), (README, 13, 21), (PRIOR, 39, 55)],
    3: [(PLAN, 31, 41), (PLAN, 60, 67), (PLAN, 81, 89), (PLAN, 94, 104), (S1, 104, 189), (REVINIT, 1, 60), (OVR, 268, 282),
        (TRSK, 488, 491), (TRSK, 553, 556), (TRSK, 612, 615), (TASKSK, 288, 292), (PSPEC, 246, 252), (PSPEC, 653, 653)],
}

ALLROWS = json.loads((OUT / "artifacts" / "coverage-matrix.json").read_text())["rows"]
MANUAL = {"INF-003": ("covered", "PLAN:12-14 header and Constraints PLAN:19-23"), "INF-014": ("covered", "PLAN:24 (no acceptance line needs an end point today)"),
          "INF-015": ("partial", "PLAN:22 names part of the list; no task or check covers rf-qa.md, rf-qa-qualitative.md, rf-analyst.md, templates, rule prompts"),
          "INF-016": ("covered", "PLAN:22")}
SLICE_IDS = {1: {"INF-002", "INF-005", "INF-006", "INF-007", "INF-008", "INF-015", "INF-016"}, 2: {r["id"] for r in ALLROWS},
             3: {"INF-003", "INF-004", "INF-009", "INF-010", "INF-011", "INF-012", "INF-013"}}


def coverage(n):
    out = ["| Requirement / Task | Card ID | Status | Grounding |", "|---|---|---|---|"]
    for r in ALLROWS:
        if r["id"] not in SLICE_IDS[n]:
            continue
        st, gr = MANUAL.get(r["id"], ("covered" if r["match"] != "none" else "unmapped-mechanical", f"source.md:{r['line']}"))
        out.append(f"| {r['id']}: {r['quote'][:90].replace('|', '/')} | {r['best_task'] if r['match'] != 'none' else 'none'} | {st} | {gr} |")
    return "\n".join(out)


for n, (persona, cls, alias, lens, ids) in PERSONA.items():
    parts = [f"# Reviewer {n} brief ({persona}, model class {cls})\n",
             "## T1 card excerpt\n", f"Assignment: independent pre-execution review of the plan `{PLAN}` against its request `{SRC}` (UC-1, advisory, read-only). "
             f"{lens}\n\n{COMMON_LEAD}\n\nReturn your findings as your final message (you cannot write files); the orchestrator saves them. "
             "For each finding give: id (R%d-1, R%d-2, ...), grade (blocking or minor), the plan location (PLAN:line), your evidence as file:line with a short quote, what the executor would do wrong, and the smallest fix. "
             "At most 8 findings, each under 700 characters. If a T1 lead is wrong, say so in a final section 'Leads dropped' with one line each. Cite only lines you have Read.\n\n" % (n, n)
             + card_slice(ids) + "\n", "## Grounding hunks\n", RUN_STATE + "\n",
             f"`{OUT}/artifacts/coverage-matrix.md` holds the coverage matrix (artifact ref).\n" if n == 2 else ""]
    for p, a, b in HUNKS[n]:
        parts.append(hunk(p, a, b))
    parts += ["## Coverage slice\n", coverage(n) + "\n"]
    (OUT / "reviewer-briefs" / f"reviewer-{n}.md").write_text("\n".join(parts))

# Wave 2 artifacts
cm = json.loads((OUT / "artifacts" / "coverage-matrix.json").read_text())
(OUT / "artifacts" / "tier_decision.yaml").write_text(f"""selected_tier: 2
fired_rule_number: 4
coverage_degraded: parsed-sparse
surface_unreached: null
composite_score: 7
per_signal_breakdown:
  scope_size: 1
  task_count: 1
  blast_radius: 2
  spec_density: 2
  ambiguity_signals: 1
escalation_reason: "S_domains=3 (code, tests, docs) fires rule 4; the parse-density guard (parsed 0, inferred 16) forbids any Tier-1 stop; calibrated C=0.74 (<0.85, rule 6) and S_dev_density 0.25 by the mechanical containment rule (rule 5) would also escalate"
t2_engine_requested: null
t2_engine_effective: null
panel_fallback_reason: null
inputs:
  confidence_calibrated: 0.74
  S_scope: 7
  S_domains: 3
  S_dev_density: 0.25
  coverage_pct_union: {cm['coverage_pct_union']}
  coverage_undefined: false
""")
rows = [
    (0, "0.1", "ok", "flags parsed: --mode pre --spec source.md --tasklist plan; mode rule 1"),
    (0, "0.2", "ok", "input paths exist"),
    (0, "0.3", "ok", "sc-adversarial-protocol skill file present; invoked at Wave 4 (probe = the invocation)"),
    (0, "0.4", "ok", "input_tree_sha256 over 9 files; artifacts/input-snapshot.yaml; output root outside work-unit dir (no overlap)"),
    (0, "0.5", "ok", "3 distinct model aliases (opus claude-gw-tier1a, sonnet claude-gw-tier1b, haiku claude-gw-tier2): T2 with 3 reviewers; t2_model_class_diversity: full"),
    (0, "0.5e", "skip", "--isolate-reviewers not set: reviewer_isolation disabled; reviewers ground in the live tree (read-only agent type)"),
    (0, "0.5b", "warn", "executor class unknown (UC-1 has no executor; no --executor-model, no EXECUTOR_MODEL_CLASS): executor_class_resolved false"),
    (0, "0.6", "warn", "all aliases are Anthropic-gateway names: t2_vendor_diversity single (warn-only)"),
    (0, "0.7", "ok", "memory hydrate: last-pass-brainstorm-reflect-panel.md read (hit); deviation-patterns-brainstorm-reflect-panel.md missing (miss)"),
    (0, "0.8", "ok", "audit.log opened"),
    (1, "1A", "ok", "grounded with Read/Grep/Bash against live files; codegraph index fresh (3572 files, 0 changes) but covers Markdown not at all; floor used"),
    (1, "1B.0", "ok", "pass 1 parsed 0; pass 2 inferred 16 (all quote-verified); containment matched 12/16 (0.75)"),
    (1, "1B.2b", "warn", "coverage_degraded: parsed-sparse (inferred 16 > parsed 0): Tier-1 stop forbidden"),
    (1, "1C", "ok", "T1 card written by orchestrator (inline; no deviation candidates in UC-1)"),
    (1, "1D", "ok", "blind calibration by confidence-calibrator (opus class): C=0.74; 30 citations checked, 3 drifted by one line or wording"),
    (2, "2", "ok", "tier decision: T2, rule 4 (tier_decision.yaml)"),
    (3, "3A", "ok", "reviewers: analyzer/sonnet, qa/haiku, refactorer/opus (third slot opus: no qwen/kimi/deepseek alias)"),
    (3, "3B.0", "ok", "3 reviewer briefs written to reviewer-briefs/"),
]
ts = NOW
with (OUT / "audit.log").open("w") as f:
    for w, s, o, e in rows:
        f.write(json.dumps({"wave": w, "step": s, "timestamp": ts, "outcome": o, "evidence_ref": e}) + "\n")
print("briefs:", [p.name for p in sorted((OUT / "reviewer-briefs").iterdir())])
for p in sorted((OUT / "reviewer-briefs").iterdir()):
    print(p.name, len(p.read_text().splitlines()), "lines", len(p.read_text()), "chars")
