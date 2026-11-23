# Reflect Reviewer - Deviation Findings
Reviewer persona: refactorer, pre-execution two-source-file boundary, dependencies, reuse, matching docs
Requested model: opus
Independent calibrated confidence: 0.87 (reviewer-3-calibration.md); calibrator_diversity=degraded.
Grounding root: /home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s (live, reviewer_isolation=disabled)
Diff scope: proposed plan against source.md; no product diff
Timestamp supplied by reviewer: 2026-11-23T18:30:00Z (UNVERIFIED reviewer metadata, not used as clock evidence)
Verdict: FAIL
Total deviations: 4 (1 Blocking, 3 Medium)

## Deviations
| # | Category | Location | What diverged | Evidence | Severity |
|---|---|---|---|---|---|
| 1 | Drift | Plan20,79,81,84 | Blocking (Decision + Missing): Task4 forbids changes outside three docs and says no installed skill changes required. Two active swarm-wizard reference tables still name /sc:code-review --apply for refactor-find; wizard uses them to pick lens and follow-up. Source requires matching documentation. Task4 could pass while wizard recommends missing command. Add both ref rows, sync-dev without staging generated .claude, remove no-skill-changes assertion, change known occurrence count four to six. | src/superclaude/skills/sc-swarm-wizard-protocol/refs/cli-contract.md:44; src/superclaude/skills/sc-swarm-wizard-protocol/refs/interview.md:65; source.md:1; plan81,84 | HIGH |
| 2 | Drift | Plan79 | Medium: wizard-guide.md:216 broad follow-up list no longer true after fix, because only refactor-find uses code-review. Plan says only three docs. Reviewer treats /code-review as real built-in per plugins/superclaude/commands/help.md:85; no lens named so not Blocking. | docs/swarm/wizard-guide.md:216; lens templates | MEDIUM |
| 3 | Drift | Plan60 | Medium: bundled-default provenance unspecified. Scaffold writes lens default through _build_spec_from_lens. Treating all spec input as caller-owned would leave placeholder in documented scaffold-to-stdin flow; no specific scaffold test. Suggested template equality plus absent compare_files and scaffold-to-stdin case. | commands.py:929,3736,2141-2144; docs/swarm/command-reference.md:82; docs/swarm/operator-runbook.md:55 | MEDIUM |
| 4 | Drift | Plan62,34 | Medium: consumer interface defines comma list, not quoting rule. Test parser/docs could pick different forms. Suggested whole-list double quotes shared between parser and docs. | src/superclaude/commands/adversarial.md:15,39,58 | MEDIUM |

## Adherence summary
Eight spec units audited: replacement, real filenames refactor-only, sibling preservation, overrides, matching docs, before/after regression full command/inputs, repaired proof, no implementation/commit/push. Fully adherent5 (1,3,6,7,8), Authorized expansion1 (count/path/empty-suggestion guards follow consumer interface), Necessary0, Drift2 (matching docs and precision of filenames/overrides), Regression0.

## What checked and sound
- Two-source-file production boundary: refactor_find.py:53 only lens template, commands.py:2129-2144 fresh builder. Resume commands.py:2578-2586 passes no template, so suggestion empty. Leaving it untouched leaves no stale command there.
- reduce.py:448-467 format_map fallback passes unknown placeholders through. Reuse sufficient, no new mechanism.
- Task dependency chain executable in principle: red test, template-only partial green, list repair full green, docs from actual output. No cycles or missing dependency.
- No current test pins stale refactor command or prefix. Bare-review golden fixtures retain prefix intentionally.
- Four named docs occurrences verified; release-notes-v1.md:34 and historical william.md:50 properly excluded.
- No new component, framework, CLI flag or lens field.

## Notes
All tests and repaired results future, not missing current deliverables. No unverified spec unit or missing hunk. No advisory correctness gaps.
