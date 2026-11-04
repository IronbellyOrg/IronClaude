# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis (opus, independent)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | The claim Wave 4 analysis report is the only file a worker might write beyond the eight named files | UNADDRESSED | MEDIUM | Create-mode jobs run `/sc:analyze` with no output name: `src/superclaude/agents/issue-worker-t1.md:22`, `:24`; `issue-worker-t2.md:24`; `issue-worker-t3.md:23`; `refs/create.md:51-53`. `commands/analyze.md:46` ("Write: Report generation"), `:22` (`--format report`), `:103` ("Analysis report"). A worker could invent `ANALYSIS.md` or `report.md`; the static test cannot see an invented name. |
| INV-002 | interaction_effects | Defining `<scope>` skill-wide as "last path segment" is safe | UNADDRESSED | MEDIUM | `refs/chains.md:7` defines `<scope>` as the main path and passes it to `/sc:troubleshoot --scope <scope>` (`:14-16`); a skill-wide redefinition would change that behaviour (plan Constraints, line 19). Limit the last-segment rule to `analysis/` file names. |
| INV-003 | guard_conditions | `written_md_names` collects every file name a worker is told | UNADDRESSED | LOW | Plan line 68 scans only backtick spans and `.md` tokens; plain-text names escape. Today all names are in code spans. |
| INV-004 | collection_boundaries | Templates are not a place where a worker learns a file name | UNADDRESSED | LOW | Workers fill templates (`issue-worker-t1.md:31`); `templates/summary.md:20` will carry the analysis name; plan line 70 leaves `templates/*.md` out of the blocked-name scan. |
| INV-005 | guard_conditions | The tool-input paragraph pins the analysis name | ADDRESSED (claim mode only) | LOW | Plan line 25 ("such as"), line 52 (mandatory in claim job 1 of t1/t2); create jobs not covered (see INV-001). |
| INV-006 | sufficiency_challenge | The orchestrator's spawn prompt will name a safe analysis path | ADDRESSED (partly) | LOW | `SKILL.md:66` requires each exact path in spawn prompts; no check covers create-mode spawn prompts (`refs/create.md`). |
| INV-007 | state_variables | The stale-copy handoff note concerns skills only | UNADDRESSED | LOW | `src/superclaude/cli/install_agents.py:51` and `install_commands.py:55` also skip existing files without `--force`; the note should name agents and the command. Nothing installed on this machine today. |
| INV-008 | count_divergence | Ten pre-fix copies and eight worker names stay consistent | ADDRESSED | LOW | Plan line 31 lists 10 files; `_WORKER_FILES` (`tests/skills/test_issue_worker_agents.py:228-237`) and the Constraints paragraph list the same 8 names. |
| INV-009 | guard_conditions | The `## Outputs` scan finds its heading | ADDRESSED | LOW | `src/superclaude/commands/issue.md:62`; empty-scan risk covered by consensus item 6. |
| INV-010 | collection_boundaries | `<REPORT.md` at `refs/chains.md:14` escapes only because of `<` | ADDRESSED | LOW | Covered by consensus item 7 (probe case). The file is written by `/sc:troubleshoot` in the user's session, not a worker. |

## Summary

- **Total findings**: 10
- **ADDRESSED**: 5 (INV-005 and INV-006 partly)
- **UNADDRESSED**: 5
  - HIGH: 0
  - MEDIUM: 2 (INV-001, INV-002) — warning, does not block convergence
  - LOW: 3 (INV-003, INV-004, INV-007)
- Orchestrator note (verified 2026-11-04T18:51Z): the create-mode `/sc:analyze` mentions at `issue-worker-t1.md:22,24`, `issue-worker-t2.md:24`, `issue-worker-t3.md:23` and `refs/create.md:51-53` exist as cited.
