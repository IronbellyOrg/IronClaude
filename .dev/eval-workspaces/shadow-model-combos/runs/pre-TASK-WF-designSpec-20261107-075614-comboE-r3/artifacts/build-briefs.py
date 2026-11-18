import json, sys
out = sys.argv[1]
base = ".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/"
S = base + "source.md"; P = base + "TASK-WF-designSpec-20261107-075614.md"
spec = open(S).read().split("\n"); plan = open(P).read().split("\n")
cm = json.load(open(out + "/artifacts/coverage-matrix.json"))
CG = ("codegraph run state: index_state=fresh checked_at=2026-11-13T05:13:00Z "
      "worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel "
      "projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel")

ATTR = ("Attribution note: this package already executed (landed in commit 0b8a5801d, parent 0e486ab8d). The spec facts F1-F13 were re-read at the parent "
        "commit and hold there (EventType has 43 members at the parent, `conflicts.py` imports only `.fsm` and `.models`, `recovery.py` defines "
        "`BRANCH_A_LANDED`, `BRANCH_B_NOT_LANDED`, `BRANCH_C_AMBIGUOUS`, `merge_guard.py` does not exist at the parent). HEAD now carries the implementation, so a "
        "citation of HEAD code as a plan defect must be checked against 0e486ab8d (`git show` is not available to you; if you cannot check, mark the claim as inferred). "
        "You audit the PLAN and SPEC text, not the shipped code. Rules for claims: before you say an acceptance criterion \"cannot fail\" or \"is missing\", quote the "
        "criterion text first (a claim of that kind whose quote is absent will be dropped); a constraint stated in task prose without an acceptance criterion is a MINOR gap "
        "unless a wrong outcome follows.")

COV = ("Coverage (Step 1B.0): 0 parsed requirement IDs (the spec uses FR/F/G/O labels), 61 inferred rows INF-001..INF-061 with verbatim quotes "
       "(artifacts/coverage-matrix.json); containment matching covered 54 of 61 (`coverage_pct_union` 0.8852). `coverage_degraded: parsed-sparse`, so no Tier-1 stop. "
       "Unmatched rows are partly matcher noise: INF-004, INF-013, INF-018, INF-023, INF-042, INF-056, INF-057.")

INSTR = ("Write the literal heading `## Findings block` and under it ONE fence opened with exactly ```findings-v2 (never ```json, never a table), JSON lines, one object per line. "
         "Fields: id (F1, F2, ...), severity (only CRITICAL, MAJOR or MINOR; a MINOR finding is never blocking), blocking (true or false), category (one of contradiction, "
         "data-loss, missing-requirement, other, safety, unpassable-check), lens \"reflect-pre\", claim (one line, at most 300 characters), refs (requirement ids such as INF-012 "
         "or spec labels, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote of at most 200 "
         "characters; use the exact repo-relative paths printed in the H3 headings of your grounding hunks, and take line numbers from the real file: every H3 range below starts at "
         "the real file line, so never count lines inside this brief; if unsure, Read the file and check). Example line: "
         "{\"id\":\"F1\",\"severity\":\"MAJOR\",\"blocking\":false,\"category\":\"contradiction\",\"lens\":\"reflect-pre\",\"claim\":\"Task 3 says X but task 5 says Y.\","
         "\"refs\":[\"INF-012\"],\"citations\":[{\"role\":\"plan\",\"path\":\"plan.md\",\"line_start\":10,\"line_end\":12}]}. "
         "After the block add a line `coverage_rows_checked:` listing the INF row ids of your coverage slice you verified (comma separated), then a line "
         "`reviewer_model_self_report:` stating the model you are running as in one line. Return the whole card as your reply text; do not write or edit any file.")

personas = {
 1: ("analyzer", (1, 20),
     "Persona: analyzer. You audit root causes and deviations between spec and plan: interface holes, decision tables that a literal implementer would build wrongly, "
     "places where the plan restates the spec with a different signature or rule.",
     ["H2. Cycle-id continuity is asserted by prose only. The spec says the SKILL mints one id at the end of Wave 3 and the push triad and `rereview_requested` reuse it "
      "(source.md:251) and `held_cycle_published` (source.md:108) matches on that id; Task 8 prose (plan:124) says so but its AC (plan:127) only requires the ref to name the single place where the id is minted.",
      "H3. `resume_decision` row 4 re-enters `release_decision` (source.md:166), which needs `target_sha`, `applied_edits` and `cycle_id` (source.md:107), but the `resume_decision` "
      "signature (source.md:109, repeated at plan:70) carries none of them. Task 4 AC (plan:77) tests the row-4 result without saying where those values come from.",
      "H4. `settled(ready, skipped, not_applied)` returns to `HELD` \"or `RELEASE_PENDING` when a failed release preceded it\" (source.md:201); Task 3 AC (plan:60) tests only the `HELD` outcome.",
      "H9. The request key `guard:<run_id>:<cycle_id>:<to>:a<k>` (source.md:184) and the `--read` JSON to `GuardRead` mapping (source.md:88-90, source.md:230) have no named owner among the pure functions (source.md:99-110)."],
     [(S, 71, 210)]),
 2: ("qa", (21, 41),
     "Persona: qa. You audit coverage and acceptance: AUDIT the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the "
     "matrix (parsed or inferred) as a finding, and judge whether each acceptance criterion can fail mechanically.",
     ["H1. Task 11 gates three of its twelve named tests by name only: AC1 (plan:169) requires that the twelve names exist; the prose (plan:166) lists no release-failure retry "
      "(source.md:315), no unreadable-timeline-never-readies case (source.md:317) and no moved-head case (source.md:319).",
      "H5. Task 7 AC (plan:111) lists the `autoMergeRequest` key but not its type; the spec prints a boolean (source.md:230) while `gh pr view --json autoMergeRequest` returns an object or null.",
      "H6. The constraint \"protocol prose carries no `file:NNN` pointers\" (plan:23, source.md:369) has no matching AC: Task 8 AC (plan:128) tests `src/superclaude`, fences and gh scope only.",
      "H7. Task 2 AC3 (plan:49) greps \"43\" and expects no claim that the enum has 43 members; the parent models.py also has a comment about the 42nd-43rd members, so the grep keeps matching a true statement.",
      "H8. Task 7 text makes adding the script to `_RESOLUTION_SCRIPTS` conditional (plan:108) but its AC (plan:113) says the script passes the `_RESOLUTION_SCRIPTS` tests."],
     [(S, 1, 378)]),
 3: ("refactorer", (42, 61),
     "Persona: refactorer. You audit structure and tech debt in the plan: dependency order and `Depends on:` completeness, file ownership across tasks, edit-order hazards between "
     "tasks that touch the same file, pins and sync steps that a later task can break, test hygiene.",
     ["H2. Cycle-id continuity: the spec says the SKILL mints one id and the push triad and `rereview_requested` reuse it (source.md:251); Task 8 prose says so (plan:124) but no AC checks the reuse.",
      "H7. Task 2 AC3 (plan:49) greps \"43\"; the parent models.py keeps the true comment \"the 42nd-43rd\" so the grep keeps matching.",
      "H8. Task 7 makes the `_RESOLUTION_SCRIPTS` entry conditional (plan:108) while its AC (plan:113) assumes it exists.",
      "Check also: every file of spec section 6 (source.md:285-299) has an owning task; each task that edits a classified line adds its `WRITE_VERB_CLASSIFICATION` entry last (source.md:255); "
      "tasks that edit the same file are ordered by `Depends on:`."],
     [(S, 211, 378)]),
}

def hunk(path, a, b, lines):
    body = "\n".join(lines[a - 1:b])
    return "### %s:%d-%d\n\n`````markdown\n%s\n`````\n" % (path, a, b, body)

for n, (name, (lo, hi), pline, hyps, spec_ranges) in personas.items():
    rows = [r for r in cm["rows"] if lo <= int(r["requirement_id"].split("-")[1]) <= hi]
    t = []
    t.append("## T1 card excerpt\n")
    t.append(pline + "\n")
    t.append(ATTR + "\n")
    t.append(COV + "\n")
    t.append("Candidate gaps from Tier 1 for your lens (hypotheses; verify or refute each, then add what is missing):\n" + "\n".join("- " + h for h in hyps) + "\n")
    t.append(INSTR + "\n")
    t.append("## Grounding hunks\n")
    t.append(CG + "\n")
    for (p, a, b) in spec_ranges: t.append(hunk(p, a, b, spec))
    t.append(hunk(P, 1, len(plan) - (1 if plan[-1] == "" else 0), plan))
    t.append("## Coverage slice\n")
    t.append("| Requirement | Quote | Citation | Matched task | Method |\n|---|---|---|---|---|")
    for r in rows:
        q = r["quote"].replace("|", "\\|")
        t.append("| %s | %s | %s | %s | %s |" % (r["requirement_id"], q, r["citation"].replace(base, "") , ", ".join(r["matched_task_ids"]) or "none", r["match_method"]))
    t.append("")
    open("%s/reviewer-briefs/reviewer-%d.md" % (out, n), "w").write("\n".join(t))
    print(n, name, len("\n".join(t)), "chars", len(rows), "rows")
