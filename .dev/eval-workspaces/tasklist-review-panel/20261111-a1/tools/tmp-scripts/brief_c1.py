import json, os, re, sys
O = sys.argv[1]
P = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614"
ROOT = os.getcwd()
spec = open(os.path.join(ROOT, P, "source.md"), encoding="utf-8").read().split("\n")
plan = open(os.path.join(ROOT, P, "TASK-WF-designSpec-20261107-075614.md"), encoding="utf-8").read().split("\n")
facts = open(os.path.join(O, "artifacts", "base-commit-facts.md"), encoding="utf-8").read().split("\n")
card = open(os.path.join(O, "t1-card.md"), encoding="utf-8").read()
cov = json.load(open(os.path.join(O, "artifacts", "coverage-matrix.json")))

def hunk(path, lines, a, b, lang="markdown"):
    body = "\n".join(lines[a - 1:b])
    fence = "````" if "```" in body else "```"
    return "### %s:%d-%d\n\n%s%s\n%s\n%s\n" % (path, a, b, fence, lang, body, fence)

def section(title_prefix):
    m = re.search(r"(?ms)^(%s.*?)(?=^F\d \(|^## |\Z)" % re.escape(title_prefix), card)
    return m.group(1).strip() if m else ""

grounding = section("## Grounding performed")
cover_sec = section("## Coverage")
F = {n: section("F%d (" % n) for n in range(1, 6)}

FIND_LINE = ("End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. "
 "Write the heading exactly `## Findings block` and open the fence with the info string exactly `findings-v2` (not json). "
 "Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), "
 "category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens \"reflect-pre\", "
 "claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, "
 "a repo-relative path, line_start, line_end and an optional quote of at most 200 characters). "
 "Example line: {\"id\":\"F1\",\"severity\":\"MAJOR\",\"blocking\":false,\"category\":\"contradiction\",\"lens\":\"reflect-pre\",\"claim\":\"Task 3 says X but task 5 says Y.\",\"refs\":[\"R-1\"],\"citations\":[{\"role\":\"plan\",\"path\":\"plan.md\",\"line_start\":10,\"line_end\":12}]}. "
 "After the block add a reviewer_model_self_report line stating the model you are running as in one line.")

PERSONA = {
 1: ("analyzer", "sonnet",
     "You are the analyzer reviewer. Look for logic defects in the design (decision tables, the fold, the toggle classifier, resume rules) and for plan steps that would make an implementer build the wrong behaviour. Trace a concrete input to a wrong output before you claim a defect."),
 2: ("qa", "haiku",
     "You are the qa reviewer. Look for acceptance criteria that cannot fail, spec requirements no task or criterion covers, and plan text that contradicts itself. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding."),
 3: ("refactorer", "opus",
     "You are the refactorer reviewer. Look at task ordering, missing or wrong `Depends on:` lines, two tasks editing the same file, edit order that breaks a test pin, scope drift beyond the spec, and structural hazards in the files the plan edits."),
}
SLICE = {
 1: [grounding, F[1], F[5]],
 2: [cover_sec, F[2], F[3], F[4]],
 3: [grounding, F[2], F[4]],
}
HUNKS = {
 1: [(P + "/source.md", spec, 99, 171), (P + "/source.md", spec, 173, 210), (P + "/TASK-WF-designSpec-20261107-075614.md", plan, 52, 90)],
 2: [(P + "/source.md", spec, 1, len(spec)), (P + "/TASK-WF-designSpec-20261107-075614.md", plan, 1, 30)],
 3: [(P + "/TASK-WF-designSpec-20261107-075614.md", plan, 1, 50), (P + "/TASK-WF-designSpec-20261107-075614.md", plan, 92, 130), (P + "/source.md", spec, 236, 301)],
}
FACTS_PATH = os.path.relpath(os.path.join(O, "artifacts", "base-commit-facts.md"), ROOT)
ROWSET = {
 1: lambda i: 15 <= i <= 27,
 2: lambda i: True,
 3: lambda i: i >= 28 or i <= 14,
}
codegraph = "codegraph run state: index_state=stale checked_at=2026-11-13T02:59:52Z worktree_root=%s projectPath=%s" % (ROOT, ROOT)

for n in (1, 2, 3):
    pers, cls, instr = PERSONA[n]
    out = ["# Reviewer %d brief (persona: %s, model class: %s)" % (n, pers, cls), "",
           "Task: Tier 2 pre-execution audit (UC-1) of a workflow plan against its driving design spec. Audit read-only: no file edits, no shell, no git.",
           "Subject: the plan %s/TASK-WF-designSpec-20261107-075614.md (13 tasks) against the spec %s/source.md (v3 design for the pr-submit merge guard)." % (P, P),
           "Attribution: both files are an archived package. Repository HEAD has moved and already contains the shipped feature; HEAD code is not evidence about the plan. Cite ONLY the plan and the spec (role `plan` or `spec`, the repo-relative paths above). The facts you need about the repo at the spec's base commit are in the base-commit facts hunk below.",
           "Rule: a claim you cannot tie to a plan or spec line is not a finding. Before you claim that a criterion cannot fail, quote the criterion text. Severity: CRITICAL only for a wrong outcome an implementer would ship; MAJOR for a gap a wrong implementation would pass; MINOR for wording or a nit.",
           "Your lens: " + instr, "",
           "## T1 card excerpt", "", "\n\n".join(s for s in SLICE[n] if s), "", FIND_LINE, "",
           "## Grounding hunks", "", codegraph, ""]
    for path, lines, a, b in HUNKS[n]:
        out.append(hunk(path, lines, a, b))
    out.append(hunk(FACTS_PATH, facts, 1, len(facts)))
    out += ["## Coverage slice", "",
            "Inferred requirement rows (parsed_count = 0, so every row is inferred; match = containment >= 0.6 against one task). Unmatched rows were read by hand by the orchestrator and look carried by a task under other wording, but you may disagree.", "",
            "| Row | Spec citation | Best task | Ratio | Match | Quote |", "|---|---|---|---|---|---|"]
    for r in cov["rows"]:
        idx = int(r["id"].split("-")[1])
        if ROWSET[n](idx):
            q = r["quote"].replace("|", "\\|")
            out.append("| %s | %s | %s | %s | %s | %s |" % (r["id"], r["citation"], r["best_task"], r["ratio"], r["match_method"], q))
    out.append("")
    open(os.path.join(O, "reviewer-briefs", "reviewer-%d.md" % n), "w", encoding="utf-8").write("\n".join(out))
    print(n, pers, cls, len("\n".join(out)))
