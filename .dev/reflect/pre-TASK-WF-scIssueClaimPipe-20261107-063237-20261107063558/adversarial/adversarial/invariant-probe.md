# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Independent fault-finder (opus), no variant advocated. Input: the Round 2 consensus (`consensus.md`), both debate records and `diff-analysis.md`. Paths: R = repository worktree root; P = the plan; S = the design (`source.md`).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | interaction_effects | Fix (b) is enough because it covers new write-verb lines only | UNADDRESSED | LOW | Orchestrator-corrected grade (probe said MEDIUM). SKILL.md:72, SKILL.md:135 and refs/claim.md:9 are among the already-classified lines (keys at tests/skills/test_worker_contract.py:2125-2181); editing any of them without updating its old key fails test_classification_table_has_no_stale_entries (:2203-2208). The probe's further claim that `--submit` makes the lines false is not established: SKILL.md:72 says the skill itself is the only writer, and the launched agent is a separate session. Only the stale-key risk stands. |
| INV-002 | guard_conditions | Tasks 2, 5 and 7 are the only tasks that add audited lines | UNADDRESSED | MEDIUM | Tasks 1, 3, 4 also edit files in AUDIT_ROOTS (test_worker_contract.py:1090-1094); the template's push and commit lines that the launched agent runs fit none of the five categories (:1103-1105); labelling them read-only is unchecked except for gh api lines (:2220-2226) |
| INV-003 | guard_conditions | The tracked-file set is always known | UNADDRESSED | MEDIUM | When `git ls-files` fails, `run()` returns a failed result and does not raise (P:34); the set reads as empty, a differing tracked file is renamed to `.prev` and overwritten; neither S:195 nor P:57 requires the copy to fail then; fix (c) has the same problem (an empty list cannot say none tracked from unknown) |
| INV-004 | count_divergence | A separate claim-mode return contract exists to be replaced with the ten fields | UNADDRESSED | MEDIUM | P:130 asks for the replacement; SKILL.md:101-115 is one contract shared in both modes and carries `status` which S:161 still needs; ST-10 only checks the ten fields are present (S:356); a literal replacement passes the test while dropping `status`, `issue_number`, `next_steps_path` or changing create mode |
| INV-005 | state_variables | "worktree JSON" in fix (c) names one thing | UNADDRESSED | LOW | It could be the subcommand's stdout (fixed key set, P:49) or the `{path,status}` record (S:197); adding the field to the record changes the record guard and the launch inputs |
| INV-006 | interaction_effects | An ST-4 scan reading one line at a time can find an orca command line in the script | UNADDRESSED | MEDIUM | Task 9's format check (P:162) wraps the launch argv list so `"--model",` sits on its own line; a line scan misses it and cannot scope the outside-the-launch-call exemption (S:350) |
| INV-007 | sufficiency_challenge | A green suite means the feature works | UNADDRESSED | HIGH | C-013 is agreed MEDIUM but none of fixes (a) to (h) covers it; the template's "check that no PR is already open" step (S:226) can be written as `gh pr list --head <branch>` with no `--repo`; the fork-safety scan covers only `_FORK_FILES` (tests/skills/test_issue_protocol.py:288, scan at tests/skills/test_issue_worker_agents.py:31-48), templates are not in that set; the launched agent could reach the upstream repository while every test passes |
| INV-008 | state_variables | One `warning` field is enough | UNADDRESSED | MEDIUM | C-004 is agreed but has no fix; the worktree step has the same collision: W-ORIGIN-BASE-STALE and the `.prev` W-WORKTREE-COPY-FAILED can both apply (P:56-59); P:59 keeps only the code that set the status, so the remedy for the other is lost |
| INV-009 | collection_boundaries | A re-claim at a new level leaves the running agent's files alone | UNADDRESSED | MEDIUM | Wave 5 rewrites launch-prompt.md (S:145) and Wave 7 copies it into the worktree (S:195) before Wave 8 returns already_launched (S:208); the running agent's prompt file then no longer matches the level in its launch record |
| INV-010 | state_variables | Pending launch-level records are cleaned up | UNADDRESSED | LOW | S:212 "The pending record stays"; the hook that would consume it (#394) is not built, so the pending store only grows |
| INV-011 | count_divergence | Flag and field counts agree | ADDRESSED | LOW | Seven flags at S:347 and Task 3 updates tests/commands/test_issue_command.py:77-80; ten fields at S:244-253; FO-5 left out deliberately (S:359); debate Round 1 (C-006) |
| INV-012 | guard_conditions | Task 3 avoids the literal `--repo` in issue.md | ADDRESSED | LOW | tests/commands/test_issue_command.py:99-103 bans it and Task 3's acceptance run (P:75) executes that test; debate U-004 |
| INV-013 | sufficiency_challenge | Gate enumeration: the fixes pass every gate between fix site and assertion site | UNADDRESSED | LOW | tests/core: the new /sc:issue row must be ASCII (tests/core/test_how_we_work_routing_table.py:342-347); plugin mirror checked by tests/commands/test_routing_plugin_parity.py (Task 9 copies byte for byte); tests/skills: the write-verb and inventory tests are the only gates and INV-001 and INV-002 are the open gaps; make lint runs ruff check after lint-architecture (Makefile:48-50), so the new script must be ruff-clean; Task 9 never runs tests/docs (P:160) |
| INV-014 | interaction_effects | The red windows between tasks close | ADDRESSED | LOW | Fixes (a) and (e); debate Round 2 (V1 and V3) and C-009 |

## Summary

- **Total findings**: 14
- **ADDRESSED**: 3 (INV-011, INV-012, INV-014)
- **UNADDRESSED**: 11
  - HIGH: 1 (INV-007)
  - MEDIUM: 6 (INV-002, 003, 004, 006, 008, 009)
  - LOW: 4 (INV-001 after the orchestrator's correction, INV-005, 010, 013)

Note: the fault-finder reported "10 open and 4 covered"; counting the table rows gives 11 UNADDRESSED and 3 ADDRESSED, because INV-013 is listed as UNADDRESSED (the Task 9 test gap). The table is authoritative.

## Gate result

Convergence status before resolution: **BLOCKED_BY_INVARIANTS** (1 HIGH unaddressed: INV-007).

Resolution by the orchestrator, recorded here so it is not read as a silent pass:

- INV-007 restates debate point C-013 (agreed Drift/MEDIUM, fix in the design first), which both advocate 1 and advocate 3 had accepted in Round 1. The orchestrator's `consensus.md` summary listed fixes (a) to (h) and left C-013 and C-004 out of the fix list by mistake; the debate itself had not left them out. The probe correctly graded the summary, not the debate.
- The consensus is amended with fix (i): the launch-prompt `submit` block names `--repo IronbellyOrg/IronClaude` on every gh call, and a test covers templates (extend `_FORK_FILES` to include `templates/launch-prompt.md` or add a pin). With (i) in place the severity of INV-007 as a reachable gap is closed; the item is raised to a **blocking** finding (security: wrong-repo exposure) in the merged verdict because the plan, as written, leaves it open.
- No Round 3 runs at depth standard. The remaining 6 MEDIUM items are warnings that do not block convergence; each becomes a refinement finding in the merged verdict (see `refactor-plan.md`).
