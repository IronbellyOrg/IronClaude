# Issue 552 review

Template: adapted issue findings skeleton from /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/550/report-template.md.

## Verdict and evidence
**verdict: in-progress.** Keep issue #552 open. The policy change and reviewer repairs are merged, but the final propagation stage is explicitly held and still has live work; the original classifier proposal has been narrowed out of the current implementation rather than delivered.

Merged evidence: PR #581 (`fc4b2240225080cbfc5e7bbc1a1f4f71cd24084d`), #582 (`64e8eacf2b3ff40be07ae9c9959071684c3765a0`), #605 (`e3e9d636adfff5c5a3d908f1e67a8ef79626f31d`), #688 (`61ac2c2e6effc24baa5ccef2a71a0a08d85bd5cd`) and evidence-preservation PR #694 (`7f0919345479007ad72724dd16b4e4cf08136e65`). All are MERGED in the GitHub reads. The current rule is at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/output-styles/pragmatic.md:240-246. The explicit hold and blank stage-four approval are at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:23-39.
## Real current state
- **Implemented:** consequence-based blocking, Medium/Note follow-ups, no rechecking non-blockers, the two-fix-cycle cap and own-scale exceptions: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/output-styles/pragmatic.md:240-246. The reflect reviewer now carries the rule and the stage-3c instructions about required behaviour and broken plan checks: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/agents/reflect-reviewer.md:117-124.
- **Observed regression check:** `uv run pytest tests/skills/test_review_severity_rule.py -q` passed all 59 tests in 3.78 seconds. This verifies text consistency and selected grading instructions, not real-world review accuracy. The eleven-carrier list and reflect-specific pins are at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_review_severity_rule.py:181-232.
- **Still inconsistent:** the QA authoring template still merges by highest label, fails on CRITICAL/IMPORTANT labels and says to fail when in doubt. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/templates/documents/agent_template_qa.md:85,100,157-163,339. The newer consequence-based rule appears beside these instructions, so passing copy tests does not prove the surrounding gate text is fixed.
- **Later progress missing from the issue's November 17 comment:** PRs #605 and #688 merged the reflect fixes; PR #694 preserved evidence; the developer guide's old rule row has already been corrected (/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/docs/developer-guide/review-severity-rule.md:20-30). Do not reopen that documentation task.
- **Existing plan, now partly stale:** the four-task stage-four package remains held. Its second task still names four skills subsequently removed by merged PR #650, commit `430eaa87f25c84f6cb319fe66f929e50b96125f0`: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/to-do/TASK-WF-blockerStage4-20261117-170451/TASK-WF-blockerStage4-20261117-170451.md:68-78. A direct search for the former technical-reference skill failed; the current source skill inventory also lacks the README, operational-guide and TDD skills. Do not execute those old edit instructions unchanged.
- **Research exists, not a production classifier:** the saved five-run stand-in report records 318 rows per run and majority agreement 58.5%, precision 37.6%, recall 92.7%; it explicitly says this was not Jev and warns that confidence is unsuitable as a gate: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/08-test/results.md:1-34,69-80. The final cuts explicitly removed the classifier and seeded-recall experiment from these packages: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:65-71. Those omissions are recorded scope reductions, not permission to silently implement the original larger proposal.
- **Known detection gap:** issue #692 is open for reviewers missing tie sorting before the top-N cut; it explicitly distinguishes a missed finding from a wrong grade. The owner deferred it for this release. Stage-four approval is still blank in the saved ledger; no later owner approval was verified.
## Concrete next steps
1. Reconcile the held stage-four plan against current source. Drop or replace its four removed-skill targets, retain the live template and prompt edits, and obtain the owner's chat go before implementation. The plan entry gate is at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/to-do/TASK-WF-blockerStage4-20261117-170451/TASK-WF-blockerStage4-20261117-170451.md:40-64.
2. Resolve the issue's original classifier criteria explicitly: either accept the recorded cuts that exclude classifier, registry and seeded-recall work, or reopen that scope as separate work. The current cuts are at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:65-71.
3. Treat issue #692 independently. It is an open detection blind spot, not proof that stage four is incomplete, and the owner deferred it for this release.
## Complexity and size
**complexity: medium; size: M.** The remaining edits are text propagation and plan reconciliation across templates and prompts, not a new service, but the stale four-skill task and owner gate prevent treating it as a small mechanical patch.
## Priority
**priority: P2.** The main rule already limits unnecessary review halts, while the remaining inconsistency affects newly generated QA instructions and the held plan; it does not block current review operation. Issue #692 is a separate P2-class detection gap, not a reason to raise this whole program to urgent.
## Dependencies
- **Needs:** an owner decision and updated stage-four plan before implementation. It also needs explicit acceptance of the recorded classifier cuts, or a separate decision to restore that scope.
- **Does not depend on:** issue #692 to continue stage four. #692 tracks a deferred reviewer detection blind spot and can remain open independently.
- **Related future capability:** issue #553, the default Jev plugin installation, would support a later classifier but is explicitly out of scope for using Jev in review gates. #552 does not block #553.
## Related issues
- #692: open; deferred reviewer blind spot for tie sorting before a top-N cut.
- #549 and #520: open; related review-panel consolidation and centralization, not prerequisites found in the current stage ledger.
- #346: closed; historical review-loop convergence issue named by the original feature request.
- #553: open; default Jev installation. Its body explicitly leaves Jev use in review gates to #552.
- #487: named in the original issue as related reusable evaluation work. Its current state was not rechecked in this pass and is UNVERIFIED.
## Related PRs
- #581: merged, `fc4b2240225080cbfc5e7bbc1a1f4f71cd24084d`; stages 0 and 1, safety scan and print-only follow-up.
- #582: merged, `64e8eacf2b3ff40be07ae9c9959071684c3765a0`; stage 3 rule rewrite and fixcheck.
- #605: merged, `e3e9d636adfff5c5a3d908f1e67a8ef79626f31d`; stage 3b reflect reviewer rule.
- #688: merged, `61ac2c2e6effc24baa5ccef2a71a0a08d85bd5cd`; stage 3c required-behaviour and broken-plan-check instructions.
- #694: merged, `7f0919345479007ad72724dd16b4e4cf08136e65`; preserves cited review evidence and the stage-four route debate.
- #650: merged, `430eaa87f25c84f6cb319fe66f929e50b96125f0`; removes four skills still named by the held stage-four plan. It is related through plan staleness, not a blocker-rule implementation PR.
## Verification limits and negative evidence
- No later GitHub timeline event was checked beyond the issue body, both comments and selected issue/PR reads. A stage-four owner approval after the saved ledger is UNVERIFIED; the ledger itself still shows the approval cell blank.
- The installed `~/.claude` output style was not compared with source, so whether every machine has refreshed its copy is UNVERIFIED.
- The original 109-occurrence count was not remeasured. The issue itself already says that count was unverified, and this pass did not search every severity phrase across the repository.
- The 59 passing static tests do not prove live reviewers catch or correctly grade every defect. No new review run was performed.
- Codegraph was stale and was not used. The cited file lines were read directly.
