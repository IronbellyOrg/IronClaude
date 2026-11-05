# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: an independent agent on the default model; it is not an advocate. Input: the six Round 1 and Round 2 statements, diff-analysis.md, plan, spec and the sc-implement-protocol executor files. The orchestrator re-Read these evidence anchors itself: managed-workspace.md:36, qa.md:83-87, qa.md:245-248, ledger.md:60, plan:23, :42, :44, :49, :91, :112, :121, :209-236, source.md:149, :296, :303-310, and the gh `--limit` default of 30 (`gh pr list --help`, `gh label list --help`). INV-009 rests on inferred CPython behaviour that was not run.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Moving the suite/lint/sync/staging task ahead of Tasks 14 and 15 resolves C-001 on its own | UNADDRESSED | HIGH | Task 16 is the only `git add .dev/tasks` step (plan:236). The package and its `artifacts/` are always staged (plan:23; managed-workspace.md:36). After the reorder, `t14-tier-smoke.md` and `t15-clickup-smoke.md` would be written after staging and left unstaged. Task 15 may update the fixtures and the script (plan:219), but its AC re-runs only one test file (plan:224), so a script edit would get no sync-dev, verify-sync, lint or full pytest run (source.md:400, :475). |
| INV-002 | sufficiency_challenge | The reorder alone removes the "reported as blocked" contradiction | UNADDRESSED | HIGH | plan:213 and :223 still require "blocked rather than passed". `complete` is allowed only with `compliant` (ledger.md:60). A truthful E-TIER-UNAVAILABLE row satisfies an evidence AC (qa.md:83-87), which gives a silent pass. An unmet AC instead goes to the fix pass, the repair round, the ladder and then E-HALT-QA (qa.md:245-247). With the smoke tasks last, a halt also blocks the managed archive gate (managed-workspace.md:47, :61). |
| INV-003 | interaction_effects | Having the user export the token before the session resolves A-001 with no side effects | UNADDRESSED | HIGH | The Task 2 no-token check only says "With `CLICKUP_API_TOKEN` unset" (plan:49) and does not force it. With the token and workspace exported, the script would call `GET /user`, page through the real workspace, and `PUT` an assignment on a task that links #302 (source.md:303-309). That is an unapproved ClickUp write outside the two scheduled live checks (plan:24-25). The test file is not required to clear the environment either (plan:44). |
| INV-004 | guard_conditions | Task 15 can compare live response shapes with the fixtures without handling the secret | UNADDRESSED | MEDIUM | The script prints only status JSON (plan:42; source.md:302-310). Getting the raw shapes needs ad-hoc authenticated calls, and personal `GET /user` data could end up in committed fixtures (plan:219) or in the transcript. |
| INV-005 | interaction_effects | The C-002 fix (run ACs 3 and 4) is safe to add | UNADDRESSED | MEDIUM | plan:25 says "The only live checks in this plan are the two the source schedules", so a new live task conflicts with that constraint. AC 3 needs the Wave 1 T3 spawn (source.md:147, :155), so it has the same session and tier dependency as Task 14 (plan:209). If the guard is faulty, the run reaches `gh issue edit --add-assignee` (source.md:162). |
| INV-006 | count_divergence | Adding the never-pass-`model` rule to claim.md and create.md satisfies "every ref" | UNADDRESSED | LOW | There are five refs (plan:91-95). source.md:132 says "SKILL.md and every ref". The plan covers tiers.md only (plan:95, :103), and the test checks two files (plan:121). |
| INV-007 | collection_boundaries | The merged-PR list covers every PR merged since the issue was created | UNADDRESSED | MEDIUM | The `gh pr list` call at source.md:149 has no `--limit`, and the gh default is 30 (`gh pr list --help`). Task 5 copies "the gh commands exactly as written" (plan:91). The `gh label list --limit 200` at source.md:188 is explicit. |
| INV-008 | collection_boundaries | "Page through ... page=<p>" is fully specified | UNADDRESSED | MEDIUM | Neither plan:42 nor source.md:304 states the starting page. The page-cap test (plan:44) does not pin it. Behaviour for an invalid `CLICKUP_MAX_PAGES` value is undefined: exit 2 covers command-line arguments only (plan:42). |
| INV-009 | state_variables | The skill directory holds only text files when Tasks 7 and 13 scan it for `src/superclaude` | UNADDRESSED | MEDIUM | Loading the scripts by path in the tests can write `scripts/__pycache__/*.pyc` containing the absolute source path (inferred, not run). The Task 7 test (plan:121) and the Task 13 `grep -rn` (plan:198, :202) could then match. |
| INV-010 | count_divergence | "Under 500 lines" is measured the same way in the AC and the test | UNADDRESSED | LOW | The AC uses `wc -l` (plan:112) and the test counts lines in Python (plan:121). The two differ by one for a file with no final newline. |
| INV-011 | count_divergence | Plan counts match the spec | ADDRESSED | LOW | These match: 14 templates, 5 refs, 3 agents, 9 STOP codes (plan:109), 6 chains, 5 flags (plan:133) and 9 return-contract fields. |

## Summary

- **Total findings**: 11
- **ADDRESSED**: 1
- **UNADDRESSED**: 10
  - HIGH: 3 (INV-001, INV-002, INV-003)
  - MEDIUM: 5 (INV-004, INV-005, INV-007, INV-008, INV-009)
  - LOW: 2 (INV-006, INV-010)

## Gate result

CONVERGENCE BLOCKED: 3 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-002, INV-003
These invariant violations must be resolved before convergence can be declared.
Action taken: depth is standard, so no further debate round runs. The three items do not reverse the consensus. They are gaps in its recommended fixes. The orchestrator folds them into the merged recommendations: INV-001 and INV-002 into the C-001 finding, INV-003 and INV-004 into the A-001 finding. They are still reported as `unaddressed_invariants`, because the debate itself did not address them.

WARNING: 5 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-004, INV-005, INV-007, INV-008, INV-009
These items do not block convergence but should be reviewed.

## Fault-finder raw output

The full text is preserved in `.work/r25-probe.md`, next to this file.
