# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: independent opus general-purpose agent, read-only, not an advocate. Entries are condensed from its report; evidence cites lines it Read. The orchestrator re-Read the lines it relies on (plan, spec, create.md:1-12, test_issue_protocol.py:1337-1342, claude_process.py:228-243, .gitignore:76-86, CLAUDE.md:14-23 and 35-37) before adopting any entry.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | C-005 (no expected `issue create` count) changes no named check, so it is Medium | UNADDRESSED | HIGH | PLAN:90,148,171; ACC:15 (the original "hung" failure); a plain-text question that never posts shows 0 questions and 0 creates and raises no finding |
| INV-002 | interaction_effects | C-006 is Medium whichever C-001 fix is chosen | UNADDRESSED | HIGH | ACC:17; CREATE:86 ("keep the draft" leaves the body unchanged); PLAN:131; becomes Decision if runs are used to mark AC2 delivered |
| INV-003 | guard_conditions | C-007b (raw logs staged, no secret scan) is only hardening | UNADDRESSED | HIGH | PLAN:22,89,108; CLAUDE.md:37; .gitignore:79,85; claude_process.py:233-241 (operator environment passed to the child) |
| INV-004 | sufficiency_challenge | Disabling the clone's push URL and denying `git push` closes C-007a | UNADDRESSED | HIGH | PLAN:22,88,89,91,132,159; explicit-URL push ignores `pushurl`; prefix deny rules are bypassed by `git -C . push`, absolute paths or `bash -c`; the plugin-directory option keeps the real home; the PLAN:159 stop cannot fire because nothing detects an uninterceptable write |
| INV-005 | sufficiency_challenge | Relabelling Phase 1 and capping AC2/AC5 alone closes C-001 | UNADDRESSED | HIGH | PLAN:81 (says Phase 3 proves it), PLAN:171 (verdict list has no "partly evidenced" slot), PLAN:175 (bans only "a static wording test alone"), PLAN:195 (needs "partly evidenced" counted as not delivered) |
| INV-006 | collection_boundaries | A description-only run cannot exercise mixed or multiple contradictions | UNADDRESSED | HIGH | CREATE:65,71 (assumptions go to New material, so contradiction runs are often mixed), CREATE:86 (one question names every item), PLAN:92,123,131 (131 does not record whether additions are kept); several false files can induce multiple contradictions; empty notes and "changed flag" cannot be induced (CREATE:38,65) |
| INV-007 | interaction_effects | Injecting prepared notes is compatible with the plan | UNADDRESSED | HIGH | PLAN:23,93,112; SPEC:27: a stub or hook is not a `src/` file, so it conflicts with the loaded-file hash check |
| INV-008 | state_variables | PLAN:112 proves runs used the `src/` workers and skill (new; neither card found it) | UNADDRESSED | HIGH | CREATE:5,7 (workers resolve from `~/.claude/agents/`, project copy first); CLAUDE.md:18 (project `.claude/agents/` is gitignored, so absent from a clone); PLAN:23,89,108,112 (self-test has no model call and checks the harness's own list); unverified how a plugin directory resolves agents |
| INV-009 | guard_conditions | Seeding the skill, three workers and `commands/issue.md` is enough | UNADDRESSED | MEDIUM | CREATE:7,32,53-55 (`/sc:analyze`, adversarial skill) not in PLAN:89,93 |
| INV-010 | guard_conditions | No isolated runner exists | UNADDRESSED | MEDIUM | `src/superclaude/cli/eval/claude_process.py:108-112,183,233-241` is an existing isolated runner |
| INV-011 | guard_conditions | C-004 changes no verdict, so it is Medium | UNADDRESSED | HIGH | PLAN:171 vs ACC:16,19; PLAN:130,169,195 |
| INV-012 | sufficiency_challenge | A Task 4 checkpoint "when interception is unavailable" closes C-002 | UNADDRESSED | HIGH | PLAN:90,98,108,111; SPEC:35; misses a question tool that is missing or denied, non-gh writes, and a place for a revised estimate |
| INV-013 | interaction_effects | The C-002 stop and the C-011 stop are independent | UNADDRESSED | MEDIUM | PLAN:97,104,159,165,182,193 |
| INV-014 | state_variables | Moving the AC6 verdict after Task 10 fixes C-010 | UNADDRESSED | MEDIUM | ACC:21; PLAN:182,195: AC6 needs the monitored pull request, which exists only after Task 11 |
| INV-015 | count_divergence | The cited counts agree | ADDRESSED | LOW | 17 selected tests (test_issue_protocol.py:1433-1518), six criteria (ACC:16-21); hazard: `-k` can match the new module name |
| INV-016 | guard_conditions | The advocates' citations are accurate | UNADDRESSED | LOW | V2 advocate's grep claim and V1 advocate's CREATE:59 description were imprecise; CLAUDE.md:37 and .gitignore:85 accurate |
| INV-017 | guard_conditions | C-009 is a Note | UNADDRESSED | MEDIUM | PLAN:141,148; CREATE:57,86 |
| INV-018 | collection_boundaries | The plan's paths and names are unambiguous | UNADDRESSED | LOW | PLAN:68 vs test_issue_protocol.py:1337-1342 (fragment entry); PLAN:111 vs PLAN:184 (`./artifacts/` vs "from the repository root") |
| INV-019 | state_variables | The closed state of issue 834 and presence of `.dev/issues/834/` | ADDRESSED | LOW | C-003 Medium correct; `.dev/issues/834/` untracked, PLAN:25 |

## Summary

- **Total findings**: 19
- **ADDRESSED**: 2
- **UNADDRESSED**: 17
  - HIGH: 10 (INV-001, 002, 003, 004, 005, 006, 007, 008, 011, 012)
  - MEDIUM: 5 (INV-009, 010, 013, 014, 017)
  - LOW: 2 (INV-016, 018)

## Invariant gate (orchestrator)

Gate result before disposition: CONVERGENCE BLOCKED: 10 HIGH-severity UNADDRESSED invariants (INV-001, 002, 003, 004, 005, 006, 007, 008, 011, 012). Depth standard has no Round 3, so the orchestrator resolved each against the files and recorded the disposition below; the merged card applies them.

| INV | Disposition in the merged result |
|-----|----------------------------------|
| INV-001 | Fix adopted (expected create count) in M-05; grade kept Medium (PLAN:130 records retained additions, which a non-posting run fails). Grade disagreement with the fault-finder remains: counted as unresolved |
| INV-002 | Adopted as the conditional note in M-06 |
| INV-003 | Adopted: C-007b is merged into the open Safety item M-03 (an unverified safety claim stays open) |
| INV-004 | Adopted: M-03 fix widened (isolated home, no credential helper or MCP, after-run fork check, secret scan) |
| INV-005 | Adopted: M-01 fix widened (verdict word, PLAN:81, PLAN:175, PLAN:195) |
| INV-006 | Adopted: M-01 fix adds a multiple-false-facts run and a record of kept additions in contradiction runs |
| INV-007 | Adopted as a clause in M-01 verifier and fix note (stub listed apart from `src/` hashes) |
| INV-008 | Adopted as M-13 (Medium: premise unverified) |
| INV-011 | Fix adopted in M-04 (inline the criteria); grade kept Medium (PLAN:130,169 already collect the dropped evidence). Grade disagreement remains: counted as unresolved |
| INV-012 | Adopted: M-02 fix trigger widened (dry run shows no question event, or write interception cannot be shown) |
| INV-009, INV-010, INV-015 | Not adopted (see "Dropped or downgraded findings") |
| INV-013, INV-014, INV-017, INV-018 | Adopted in M-11, M-10, M-09 (grade raised to Medium) and M-18 |
| INV-016 | Citation corrections applied (no card or plan row depends on them) |

Residual HIGH items without agreement (listed in the return contract): INV-001, INV-002, INV-008, INV-011.
